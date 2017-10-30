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
    media_response = instagram_api.LastJson
    return media_response


def get_comments(instagram_api, media_id):
    instagram_api.getMediaComments(media_id)
    comments_response = instagram_api.LastJson
    return comments_response


def put_item(datastore_client, item):
    key = datastore_client.key('Content')
    content = datastore.Entity(key)
    content['type'] = 'instagram'
    content['text'] = item['caption']['text']
    content['created_at'] = item['caption']['created_at']
    content['id'] = item['id']
    content['user_id'] = item['caption']['user_id']
    content['comment_count'] = item['comment_count']
    content['favourites_count'] = item['like_count']
    return content


def put_comment(datastore_client, item):
    key = datastore_client.key('Content')
    content = datastore.Entity(key)
    content['type'] = 'instagram'
    content['text'] = item['text']
    content['created_at'] = item['created_time']
    content['id'] = item['id']
    content['user_id'] = item['from']['user_id']
    return content
