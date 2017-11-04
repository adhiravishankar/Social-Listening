from mongoengine import Document, StringField, DateTimeField, IntField, FloatField, LongField, ObjectIdField


class Content(Document):
    network = StringField(required=True)
    content_type = StringField(required=True)
    text = StringField(required=True)
    created_at = DateTimeField(required=True)
    id = StringField(required=True)
    comment_count = IntField()
    favourites_count = IntField()
    retweet_count = IntField()
    user_id = LongField()
    user_screenname = StringField()
    sentiment = FloatField(required=True)


class Keywords(Document):
    phrase = StringField(required=True)
    overall_sentiment = FloatField()
    count = IntField(required=True)
    search = ObjectIdField(required=True)


class Search(Document):
    text = StringField(required=True)
    content_count = IntField(required=True)
    overall_sentiment = FloatField(required=True)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)
