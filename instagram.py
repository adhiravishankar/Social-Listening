import os
from InstagramAPI import InstagramAPI


def query_all_posts(tag, content_collection):
    instagram_api = login()
    tags = get_tags(instagram_api, tag)
    for tag in tags:
        media = get_media(instagram_api, tag['name'])
        while True:
            contents = []
            if 'ranked_items' in media:
                for item in media['ranked_items']:
                    contents.append(put_item(item, instagram_api, content_collection))
            if 'items' in media:
                for item in media['items']:
                    contents.append(put_item(item, instagram_api, content_collection))
            if 'more_available' in media:
                media = get_next_media(instagram_api, tag['name'], media['next_max_id'])


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


def get_next_media(instagram_api, tag, next_max_id):
    instagram_api.getHashtagFeed(tag, next_max_id)
    return instagram_api.LastJson


def get_comments(instagram_api, media_id, next_max_id=''):
    instagram_api.getMediaComments(media_id, next_max_id)
    return instagram_api.LastJson


def put_item(item, instagram_api, content_collection):
    contents = []
    content ={'network':'instagram',
              'content_type': 'post',
              'text': item['caption']['text'],
              'created_at': item['caption']['created_at'],
              'id': item['id'],
              'user_id': item['caption']['user_id'],
              'comment_count': item['comment_count'],
              'favourites_count': item['like_count']}
    if content_collection.count({'id': item['id'], 'network': 'instagram', 'content_type': 'post'}) == 0:
        contents.append(content)
    if item['comment_count'] > 0:
        comments = get_comments(instagram_api, item['id'])
        while True:
            for comment in comments['comments']:
                if content_collection.count({'id': comment['pk'], 'network': 'instagram', 'content_type': 'comment'}) == 0:
                    contents.append(put_comment(comment, item['id']))
            if 'has_more_comments' in comments:
                comments = get_comments(instagram_api, item['id'], comments['next_max_id'])
            else:
                break

    print("Putting in {} posts!".format(len(contents)))
    content_collection.insert_many(contents)


def put_comment(item, item_id):
    content = {"network": 'instagram',
               "content_type": 'comment',
               "text": item['text'],
               "created_at": item['created_at'],
               "id": item['pk'],
               "media_id": item_id,
               'user_id': item['user']['pk']}
    if 'comment_like_count' in item:
        content['favourites_count'] = item['comment_like_count']
    return content
