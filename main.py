import os
import dotenv
from pymongo import MongoClient

import mongodb
import twitter2


# get query
query = "xbox one x"

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'), verbose=True)
client = MongoClient(os.environ.get('DB_HOST'), 27017)
db = client['sociallistening']

query = query.lower()
tag = query.replace(' ', '')
search = mongodb.put_search(query, db)
content_collection = db['content']

all_tweets = twitter2.query_all_tweets(query, content_collection, search)