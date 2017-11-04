import os
import dotenv
import mongoengine

import instagram
import mongodb
import twitter
import twitter2

# get query
query = "xbox one x"

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'), verbose=True)
connection = mongoengine.connect(os.environ.get('DB_NAME'), host=os.environ.get('DB_HOST'), port=27017)

query = query.lower()
tag = query.replace(' ', '')
search = mongodb.put_search(query)

# twitter2.encode_query(query)
twitter2.get_tweets(query)

instagram_api = instagram.login()
tags = instagram.get_tags(instagram_api, tag)
for tag in tags:
    contents = []
    feed = instagram.get_media(instagram_api, tag['name'])
    for item in feed['ranked_items']:
        contents.append(instagram.put_item(item))
    for item in feed['items']:
        contents.append(instagram.put_item(item))

api = twitter.setup_twitter()
results = twitter.search(api, query)

print(results)
