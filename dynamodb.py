from datetime import datetime
from decimal import Decimal


def put_search(term, db):
    search_collection = db.Table('social_listening_search')
    search = search_collection.get_item(Key={"text": term})
    if 'Item' not in search:
        search_collection.put_item(
            Item={
                "text": term,
                "content_count": 0,
                "overall_sentiment": Decimal(0.0),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        )