import os
import tweepy
from models import Content


def setup_twitter():
    auth = tweepy.OAuthHandler(os.environ.get('TWITTER_CONSUMER_KEY'), os.environ.get('TWITTER_CONSUMER_SECRET'))
    auth.set_access_token(os.environ.get('TWITTER_API_KEY'), os.environ.get('TWITTER_API_SECRET'))
    api = tweepy.API(auth)
    return api


def search(api, text):
    """

    :param api: tweepy.api
    :param text: string
    """
    results = api.search(q=text, count=100, lang='en')
    contents = []
    for result in results:
        content = Content(network='twitter',
                          text=result.text,
                          created_at=result.created_at,
                          id=result.id,
                          user_id=result.user.id,
                          retweet_count=result.retweet_count,
                          favourites_count=result.favourites_count)
        print(content)

    return contents


def search2(api, text):
    """

    :param api: tweepy.api
    :param text: string
    """
    results = api.search(q=text, count=100, lang='en')
    contents = []
    for result in results:
        content = Content(network='twitter',
                          text=result.text,
                          created_at=result.created_at,
                          id=result.id,
                          user_id=result.user.id,
                          retweet_count=result.retweet_count,
                          favourites_count=result.favourites_count)
        contents.append(content)

    return contents