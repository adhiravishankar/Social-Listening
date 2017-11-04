import os
from InstagramAPI import InstagramAPI


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


def put_item(item):
    content ={'network':'instagram',
              'content_type': 'post',
              'text': item['caption']['text'],
              'created_at': item['caption']['created_at'],
              'id': item['id'],
              'user_id': item['caption']['user_id'],
              'comment_count': item['comment_count'],
              'favourites_count': item['like_count']}
    return content


def put_comment(item):
    content = {"network": 'instagram',
               "content_type": 'comment',
               "text": item['text'],
               "created_at": item['created_time'],
               "id": item['id'] }
    return content
