import os
from InstagramAPI import InstagramAPI


def login():
    api = InstagramAPI(os.environ.get("INSTAGRAM_USERNAME"), os.environ.get("INSTAGRAM_USERNAME"))
    api.login() # login
    return api