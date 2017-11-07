import argparse
import os
import dotenv
from pymongo import MongoClient

import instagram
import mongodb
import twitter2


dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'), verbose=True)
client = MongoClient(os.environ.get('DB_HOST'), 27017)
db = client['sociallistening']

parser = argparse.ArgumentParser()
parser.add_argument('query')
parser.add_argument('--stage')

args = parser.parse_args()
query = args.query
stage = args.stage

query = query.lower()
tag = query.replace(' ', '')
search = mongodb.put_search(query, db)
content_collection = db['content']

if stage is 'i':
    instagram.query_all_posts(tag, content_collection)
else:
    twitter2.query_all_tweets(query, content_collection, search)
    instagram.query_all_posts(tag, content_collection)
