from datetime import timedelta, date
from multiprocessing.pool import Pool
from twitterscraper.query import query_tweets_once


def insert_tweets(content_collection, query, search, tweets):
    print("Now: {} , Query: {}".format(len(tweets), query))
    contents = []
    for tweet in tweets:
        content = {'network': 'twitter',
                   'text': tweet.text,
                   'created_at': tweet.timestamp,
                   'id': tweet.id,
                   'user_screenname': tweet.user,
                   'retweet_count': tweet.retweets,
                   'favourites_count': tweet.likes,
                   'replies_count': tweet.replies,
                   'search_id': search['_id']}
        if content_collection.count({'id': tweet.id, 'network': 'twitter'}) == 0:
            contents.append(content)
    if len(contents) > 0:
        content_collection.insert_many(contents)


def query_tweets(query, content_collection, search, limit=None):
    iteration = 1
    tweets = 0
    query_with_date = query
    while True:
        print("Running iteration no {}, query is {}".format(iteration, repr(query)))
        new_tweets = query_tweets_once(query_with_date, limit, tweets)
        insert_tweets(content_collection, query, search, new_tweets)
        tweets += len(new_tweets)

        if not new_tweets:
            break

        mindate = min(map(lambda tweet: tweet.timestamp, new_tweets)).date()
        maxdate = max(map(lambda tweet: tweet.timestamp, new_tweets)).date()
        print("Got tweets ranging from {} to {}".format(mindate.isoformat(), maxdate.isoformat()))

        # Add a day, twitter only searches until excluding that day and we dont
        # have complete results for that one yet. However, we cannot limit the
        # search to less than one day: if all results are from the same day, we
        # want to continue searching further into the past: either there are no
        # further results or twitter stopped serving them and there's nothing
        # we can do.
        if mindate != maxdate:
            mindate += timedelta(days=1)

        # Twitter will always choose the more restrictive until:
        query_with_date = query + ' until:' + mindate.isoformat()
        iteration += 1


def query_all_tweets(query, content_collection, search, year=2017, month=1, end=date.today()):
    """
    Queries *all* tweets in the history of twitter for the given query. This
    will run in parallel for each ~10 days.

    :param content_collection:
    :param search:
    :param year:
    :param month:
    :param end:
    :param query: A twitter advanced search query.
    :return: A list of tweets.
    """

    limits = []
    while date(year=year, month=month, day=1) < end:
        nextmonth = month + 1 if month < 12 else 1
        nextyear = year + 1 if nextmonth == 1 else year

        for i in range(1, 26, 2):
            limits.append((date(year=year, month=month, day=i), date(year=year, month=month, day=i+2)))
        limits.append((date(year=year, month=month, day=28), date(year=nextyear, month=nextmonth, day=1)))
        year, month = nextyear, nextmonth

    queries = ['{} since:{} until:{}'.format(query, since, until) for since, until in reversed(limits)]

    all_tweets = 0
    pool = Pool(20)
    try:
        for new_tweets in pool.imap_unordered(query_tweets_once, queries):
            all_tweets += len(new_tweets)
            insert_tweets(content_collection, query, search, new_tweets)
            if len(new_tweets) > 0:
                print("Got {} tweets ({} new) for {}.".format(all_tweets, len(new_tweets), new_tweets[0].timestamp))
            else:
                print("Got {} tweets ({} new).".format(all_tweets, len(new_tweets)))
    except KeyboardInterrupt:
        print("Program interrupted by user. Returning all tweets gathered so far.")

