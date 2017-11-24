import argparse
import os

import dotenv
import imageio
from datetime import date
from pymongo import MongoClient

import analyzer
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
parser.add_argument('--year2')
parser.add_argument('--month2')

args = parser.parse_args()
query = args.query
stage = args.stage
year = args.year
month = args.month
year2 = args.year2
month2 = args.month2

query = query.lower()
tag = query.replace(' ', '')
search = mongodb.put_search(query, db)
content_collection = db['content']

if stage is 'i':
    instagram.query_all_posts(tag, content_collection)
elif stage is 't':
    if month is None and year is None and year2 is None and month2 is None:
        twitter2.query_all_tweets(query, content_collection, search)
    elif month2 is None and year2 is None:
        # noinspection PyTypeChecker
        twitter2.query_all_tweets(query, content_collection, search, int(year), int(month))
    else:
        twitter2.query_all_tweets(query, content_collection, search, int(year), int(month), date(int(year2), int(month2), 1))
elif stage is 'a':
    model = analyzer.load_keras_model()
    analyzer.process_content_unfiltered(query, content_collection, model, search)
elif stage is 'l':
    analyzer.process_language_for_content(content_collection)
else:
    twitter2.query_all_tweets(query, content_collection, search)
    instagram.query_all_posts(tag, content_collection)
