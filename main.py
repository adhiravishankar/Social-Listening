import argparse
import os
import dotenv
import nltk
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

if stage is 'p':
    search_content = content_collection.find({'search_id': search['_id'], 'processed_text': None}, {'_id': 1, 'text': 1})
    for search_item in search_content:
        text = search_item['text']
        words = nltk.word_tokenize(text)
        processed_words = []
        for word in words:
            if word not in nltk.corpus.stopwords.words('english'):
                processed_words.append(word)
elif stage is 'i':
    instagram.query_all_posts(tag, content_collection)
elif stage is 't':
    twitter2.query_all_tweets(query, content_collection, search)
else:
    twitter2.query_all_tweets(query, content_collection, search)
    instagram.query_all_posts(tag, content_collection)
