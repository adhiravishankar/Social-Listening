import os
import dotenv
import mongoengine

import mongodb
import twitter2

# get query
query = "xbox one x"

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'), verbose=True)
# connection = mongoengine.connect(os.environ.get('DB_NAME'), host=os.environ.get('DB_HOST'), port=27017)

query = query.lower()
tag = query.replace(' ', '')
# search = mongodb.put_search(query)

all_tweets = 0
tweet_generator = twitter2.query_all_tweets(query)
for tweets_for_query_tuple in tweet_generator:
    tweets_for_query = tweets_for_query_tuple[0]
    query = tweets_for_query_tuple[1]
    for tweets in tweets_for_query:
        all_tweets += len(tweets)
        print("Now: {} , Total: {}, Query: {}".format(len(tweets), all_tweets, query))