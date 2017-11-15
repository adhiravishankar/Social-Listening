import argparse
import logging
import os

import boto3
import dotenv
import imageio

import instagram
import dynamodb
import twitter2_dynamodb

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
imageio.plugins.ffmpeg.download()
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'), verbose=True)
db = boto3.resource('dynamodb')

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
dynamodb.put_search(query, db)
content_collection = dynamodb.Table('social_listening_content')

if stage is 'i':
    instagram.query_all_posts(tag, content_collection)
elif stage is 't':
    if month is None and year is None:
        twitter2_dynamodb.query_all_tweets(query, content_collection, query)
    else:
        twitter2_dynamodb.query_all_tweets(query, content_collection, query, year, month)
else:
    twitter2_dynamodb.query_all_tweets(query, content_collection, query)
    instagram.query_all_posts(tag, content_collection)
