import logging
from datetime import date
from multiprocessing.pool import Pool
from twitterscraper.query import query_single_page, INIT_URL, RELOAD_URL


def encode_query(query):
    query = query.replace(' ', '%20')
    return query


def get_tweets(query):
    query_all_tweets('xbox one x', 2017, 5)


def query_tweets(query, limit=None, num_tweets=0):
    return query_tweets_once(query, limit, num_tweets), query


def query_tweets_once(query, limit=None, num_tweets=0):
    """
    Queries twitter for all the tweets you want! It will load all pages it gets
    from twitter. However, twitter might out of a sudden stop serving new pages,
    in that case, use the `query_tweets` method.

    Note that this function catches the KeyboardInterrupt so it can return
    tweets on incomplete queries if the user decides to abort.

    :param query: Any advanced query you want to do! Compile it at
                  https://twitter.com/search-advanced and just copy the query!
    :param limit: Scraping will be stopped when at least ``limit`` number of
                  items are fetched.
    :param num_tweets: Number of tweets fetched outside this function.
    :return:      A list of twitterscraper.Tweet objects. You will get at least
                  ``limit`` number of items.
    """
    logging.info("Querying {}".format(query))
    query = query.replace(' ', '%20').replace("#", "%23").replace(":", "%3A")
    pos = None
    tweets = []
    try:
        while True:
            new_tweets, pos = query_single_page(
                INIT_URL.format(q=query) if pos is None
                else RELOAD_URL.format(q=query, pos=pos),
                pos is None
            )
            if len(new_tweets) == 0:
                logging.info("Got {} tweets for {}.".format(len(tweets), query))
                return

            logging.info("Got {} tweets ({} new).".format(len(tweets) + num_tweets, len(new_tweets)))
            yield new_tweets

            if limit is not None and len(tweets) + num_tweets >= limit:
                return
    except KeyboardInterrupt:
        logging.info("Program interrupted by user. Returning tweets gathered so far...")
    except BaseException:
        logging.exception("An unknown error occurred! Returning tweets gathered so far.")

    return tweets



def query_all_tweets(query, year=2006, month=3):
    """
    Queries *all* tweets in the history of twitter for the given query. This
    will run in parallel for each ~10 days.

    :param month:
    :param year:
    :param query: A twitter advanced search query.
    :return: A list of tweets.
    """

    limits = []
    while date(year=year, month=month, day=1) < date.today():
        nextmonth = month + 1 if month < 12 else 1
        nextyear = year + 1 if nextmonth == 1 else year

        limits.append((date(year=year, month=month, day=1), date(year=year, month=month, day=10)))
        limits.append((date(year=year, month=month, day=10), date(year=year, month=month, day=20)))
        limits.append((date(year=year, month=month, day=20), date(year=nextyear, month=nextmonth, day=1)))
        year, month = nextyear, nextmonth

    queries = ['{} since:{} until:{}'.format(query, since, until) for since, until in reversed(limits)]

    pool = Pool(20)
    all_tweets = 0
    try:
        for new_tweets, query in pool.imap_unordered(query_tweets, queries):
            all_tweets += len(new_tweets)
            print("Got {} tweets ({} new). {}". format(all_tweets, len(new_tweets), query))
            yield new_tweets
    except KeyboardInterrupt:
        print("Program interrupted by user. Returning all tweets gathered so far.")

    return sorted(all_tweets)