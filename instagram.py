import os
from InstagramAPI import InstagramAPI


def login():
    api = InstagramAPI(os.environ.get("INSTAGRAM_USERNAME"), os.environ.get("INSTAGRAM_PASSWORD"))
    api.login() # login
    return api


def get_tags(instagram_api):
    instagram_api.searchTags('xboxonex')
    tags_response = instagram_api.LastJson
    return tags_response.results