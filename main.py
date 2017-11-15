import argparse
import logging
import os
import dotenv
import imageio
from pymongo import MongoClient

import instagram
import mongodb
import twitter2

# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
imageio.plugins.ffmpeg.download()
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'), verbose=True)
client = MongoClient(os.environ.get('MONGODB_CONNECTION'))
db = client['sociallistening']

parser = argparse.ArgumentParser()
parser.add_argument('query')
parser.add_argument('--stage')
parser.add_argument('--year')
parser.add_argument('--month')

args = parser.parse_args()
query = args.query
stage = args.stage
year = args.year
month = args.month

query = query.lower()
tag = query.replace(' ', '')
search = mongodb.put_search(query, db)
content_collection = db['content']

if stage is 'i':
    instagram.query_all_posts(tag, content_collection)
elif stage is 't':
    if month is None and year is None:
        twitter2.query_all_tweets(query, content_collection, search)
    else:
        twitter2.query_all_tweets(query, content_collection, search, year, month)
else:
    twitter2.query_all_tweets(query, content_collection, search)
    instagram.query_all_posts(tag, content_collection)
