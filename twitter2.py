import logging

import requests
from datetime import date
from fake_useragent import UserAgent
from twitterscraper import Tweet
from twitterscraper.query import INIT_URL, RELOAD_URL


def encode_query(query):
    query = query.replace(' ', '%20')
    return query


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
    query = query.replace(' ', '%20').replace("#", "%23").replace(":", "%3A")
    pos = None
    try:
        while True:
            new_tweets, pos = query_single_page(
                INIT_URL.format(q=query) if pos is None
                else RELOAD_URL.format(q=query, pos=pos),
                pos is None
            )
            if len(new_tweets) == 0:
                return

            yield new_tweets
    except KeyboardInterrupt:
        print("Program interrupted by user. Returning tweets gathered so far...")
    except BaseException:
        logging.exception("An unknown error occurred! Returning tweets gathered so far.")


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
        html = response.text

        tweets = list(Tweet.from_html(html))

        if not tweets:
            print("empty array")
            return [], None

        return tweets, "TWEET-{}-{}".format(tweets[-1].id, tweets[0].id)
    except requests.exceptions.HTTPError as e:
        logging.exception('HTTPError {} while requesting "{}"'.format(e, url))
    except requests.exceptions.ConnectionError as e:
        logging.exception('ConnectionError {} while requesting "{}"'.format(e, url))
    except requests.exceptions.Timeout as e:
        logging.exception('TimeOut {} while requesting "{}"'.format(e, url))
    if retry > 0:
        print("Retrying...")
        return query_single_page(url, html_response, retry-1)

    logging.error("Giving up.")
    print("empty array")
    return [], None


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

    try:
        for query in queries:
            yield query_tweets_once(query), query
    except KeyboardInterrupt:
        print("Program interrupted by user. Returning all tweets gathered so far.")

