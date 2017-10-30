from google.cloud import datastore
from oauth2client.client import GoogleCredentials


def setup_datastore():
    GoogleCredentials.from_stream('Chiroptera-a280fa6f621c.json')
    datastore_client = datastore.Client(namespace='social-listening')
    return datastore_client


def put_search(datastore_client, query):
    search_key = datastore_client.key('Search')
    search = datastore.Entity(search_key)
    search['query'] = query
    datastore_client.put(search)