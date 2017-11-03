import facebook
import os


def setup():
    return facebook.GraphAPI(access_token=os.environ.get("FACEBOOK_ACCESS_TOKEN"), version="2.10")


def search_pages(graph, query):
    return graph.search(type='page', q=query)


def search_posts(graph, page):
    return graph.get_connections()
