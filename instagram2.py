import os
import requests


def search_tags(tag):
    payload = {'access_token': os.environ.get('INSTAGRAM_ACCESS_TOKEN'), 'q': tag}
    response = requests.get('https://api.instagram.com/v1/tags/search', params=payload).json()
    return response['data']


def get_media(tag):
    response = requests.get('https://api.instagram.com/v1/tags/' + tag + '/media/recent', params=
    {'access_token': os.environ.get('INSTAGRAM_ACCESS_TOKEN')}).json()
    return response['data']

