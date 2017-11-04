from datetime import datetime


def put_search(term, db):
    search_collection = db['search']
    search = search_collection.find_one({"text": term})
    if search is None:
        search = {"text": term,
                  "content_count": 0,
                  "overall_sentiment": 0.0,
                  "created_at": datetime.now(),
                  "updated_at": datetime.now()}
        return insert(search_collection, search)
    return search


def insert(collection, item):
    id = collection.insert_one(item).inserted_id
    item['_id'] = id
    return item