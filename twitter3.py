from datetime import date

import requests
from fake_useragent import UserAgent
from twitterscraper import Tweet

INIT_URL = "https://twitter.com/search?l=en&f=tweets&vertical=default&q={q}"
RELOAD_URL = "https://twitter.com/i/search/timeline?l=en&f=tweets&vertical=" \
             "default&include_available_features=1&include_entities=1&" \
             "reset_error_state=false&src=typd&max_position={pos}&q={q}"

def query_all_tweets(query, search, content_collection):
    """
    Queries *all* tweets in the history of twitter for the given query. This
    will run in parallel for each ~10 days.

    :param query: A twitter advanced search query.
    :return: A list of tweets.
    """
    year = 2006
    month = 3

    limits = []
    while date(year=year, month=month, day=1) < date.today():
        nextmonth = month + 1 if month < 12 else 1
        nextyear = year + 1 if nextmonth == 1 else year

        limits.append((date(year=year, month=month, day=1), date(year=year, month=month, day=10)))
        limits.append((date(year=year, month=month, day=10),
             date(year=year, month=month, day=20))
        )
        limits.append(
            (date(year=year, month=month, day=20),
             date(year=nextyear, month=nextmonth, day=1))
        )
        year, month = nextyear, nextmonth

    queries = ['{} since:{} until:{}'.format(query, since, until) for since, until in reversed(limits)]

    all_tweets = []
    for new_tweets in pool.imap_unordered(query_tweets_once, queries):
        all_tweets.extend(new_tweets)


def insert_tweets(content_collection, query, search, tweets):
    print("Now: {} , Total: {}, Query: {}".format(len(tweets), all_tweets, query))
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
    content_collection.insert_many(contents)


def query_tweets_once(query, content_collection, search):
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
    print("Querying {}".format(query))
    query = query.replace(' ', '%20').replace("#", "%23").replace(":", "%3A")
    pos = None
    tweets = []
    while True:
        new_tweets, pos = query_single_page(
            INIT_URL.format(q=query) if pos is None
            else RELOAD_URL.format(q=query, pos=pos),
            pos is None
        )
        if len(new_tweets) == 0:
            return

        print("Got {} tweets ({} new).".format(len(tweets) + num_tweets, len(new_tweets)))

        insert_tweets(content_collection, query, search, tweets)


def query_single_page(url, html_response=True, retry=3):
    """
    Returns tweets from the given URL.

    :param url: The URL to get the tweets from
    :param html_response: False, if the HTML is embedded in a JSON
    :param retry: Number of retries if something goes wrong.
    :return: The list of tweets, the pos argument for getting the next page.
    """
    headers = {'User-Agent': UserAgent().random}

    try:
        response = requests.get(url, headers=headers)
        if html_response:
            html = response.text
        else:
            json_resp = response.json()
            html = json_resp['items_html']

        tweets = list(Tweet.from_html(html))

        if not tweets:
            return [], None

        if not html_response:
            return tweets, json_resp['min_position']

        return tweets, "TWEET-{}-{}".format(tweets[-1].id, tweets[0].id)
    except requests.exceptions.HTTPError as e:
        print('HTTPError {} while requesting "{}"'.format(e, url))
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError {} while requesting "{}"'.format(e, url))
    except requests.exceptions.Timeout as e:
        print('TimeOut {} while requesting "{}"'.format(e, url))
    if retry > 0:
        print("Retrying...")
        return query_single_page(url, html_response, retry-1)

    print("Giving up.")
    return [], None