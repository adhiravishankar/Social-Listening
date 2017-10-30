import os
import dotenv
import requests

import gcloud
import instagram
import twitter

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'), verbose=True)

query = "xbox one x"
query = query.lower()
tag = query.replace(' ', '')

instagram_api = instagram.login()
tags = instagram.get_tags(instagram_api)

datastore_client = gcloud.setup_datastore()
gcloud.put_search(datastore_client, query)

api = twitter.setup_twitter()
results = twitter.search(api, datastore_client, query)

print(results)
