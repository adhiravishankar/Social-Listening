import os
import tweepy
from google.cloud import datastore

# You must use Python 2.7.x
# Rate limit chart for Twitter REST API - https://dev.twitter.com/rest/public/rate-limits


def setup_twitter():
    auth = tweepy.OAuthHandler(os.environ.get('TWITTER_CONSUMER_KEY'), os.environ.get('TWITTER_CONSUMER_SECRET'))
    auth.set_access_token(os.environ.get('TWITTER_API_KEY'), os.environ.get('TWITTER_API_SECRET'))
    api = tweepy.API(auth)
    return api


def search(api, datastore_client, text):
    """

    :param datastore_client: datastore.Client
    :param api: tweepy.api
    :param text: string
    """
    results = api.search(q=text, count=100, lang='en')
    contents = []
    for result in results:
        key = datastore_client.key('Content')
        content = datastore.Entity(key)
        content['type'] = 'twitter'
        content['text'] = result.text
        content['created_at'] = result.created_at
        content['id'] = result.id
        content['user_id'] = result.user.id
        content['retweet_count'] = result.retweet_count
        content['favourites_count'] = result.favourites_count
        contents.append(content)

    return contents


def search2(api, datastore_client, text):
    """

    :param datastore_client: datastore.Client
    :param api: tweepy.api
    :param text: string
    """
    results = api.search(q=text, count=100, lang='en')
    contents = []
    for result in results:
        key = datastore_client.key('Content')
        content = datastore.Entity(key)
        content['type'] = 'twitter'
        content['text'] = result.text
        content['created_at'] = result.created_at
        content['id'] = result.id
        content['user_id'] = result.user.id
        content['retweet_count'] = result.retweet_count
        content['favourites_count'] = result.favourites_count
        contents.append(content)

    return contents