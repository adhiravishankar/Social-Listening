from datetime import datetime

from models import Search


def put_search(term):
    search = Search.objects(text=term).first()
    if search is None:
        search = Search(text=term,
                        content_count=0,
                        overall_sentiment=0.0,
                        created_at=datetime.now(),
                        updated_at=datetime.now())
        search.save()
    return search