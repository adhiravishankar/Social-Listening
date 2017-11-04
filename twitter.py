import os
import tweepy


def setup_twitter():
    auth = tweepy.OAuthHandler(os.environ.get('TWITTER_CONSUMER_KEY'), os.environ.get('TWITTER_CONSUMER_SECRET'))
    auth.set_access_token(os.environ.get('TWITTER_API_KEY'), os.environ.get('TWITTER_API_SECRET'))
    api = tweepy.API(auth)
    return api