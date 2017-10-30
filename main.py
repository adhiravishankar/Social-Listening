import os
import dotenv

import gcloud
import instagram
import twitter

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'), verbose=True)
datastore_client = gcloud.setup_datastore()

query = "xbox one x"
query = query.lower()
tag = query.replace(' ', '')

instagram_api = instagram.login()
tags = instagram.get_tags(instagram_api, tag)
for tag in tags:
    contents = []
    feed = instagram.get_media(instagram_api, tag['name'])
    for item in feed['ranked_items']:
        contents.append(instagram.put_item(datastore_client, item))
    for item in feed['items']:
        contents.append(instagram.put_item(datastore_client, item))

gcloud.put_search(datastore_client, query)

api = twitter.setup_twitter()
results = twitter.search(api, datastore_client, query)

print(results)
