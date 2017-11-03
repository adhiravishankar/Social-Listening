import os
from InstagramAPI import InstagramAPI
from google.cloud import datastore


def login():
    api = InstagramAPI(os.environ.get("INSTAGRAM_USERNAME"), os.environ.get("INSTAGRAM_PASSWORD"))
    api.login() # login
    return api


def get_tags(instagram_api, query):
    instagram_api.searchTags(query)
    tags_response = instagram_api.LastJson
    return tags_response['results']


def get_media(instagram_api, tag):
    instagram_api.tagFeed(tag)
    return instagram_api.LastJson


def get_comments(instagram_api, media_id):
    instagram_api.getMediaComments(media_id)
    return instagram_api.LastJson


def put_item(datastore_client, item):
    key = datastore_client.key('Content')
    content = datastore.Entity(key)
    return content


def put_comment(datastore_client, item):
    key = datastore_client.key('Content')
    content = datastore.Entity(key)
    return content
