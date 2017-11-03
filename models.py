from pymodm import MongoModel, fields


class Content(MongoModel):
    network = fields.LineStringField
    text = fields.MultiLineStringField
    created_at = fields.DateTimeField
    id = fields.LineStringField
    comment_count = fields.IntegerField
    favourites_count = fields.IntegerField
    retweet_count = fields.IntegerField
    user_id = fields.BigIntegerField
    sentiment = fields.FloatField


class Keywords(MongoModel):
    phrase = fields.LineStringField
    overall_sentiment = fields.FloatField
    count = fields.IntegerField
    search = fields.ObjectIdField


class Search(MongoModel):
    text = fields.LineStringField
    content_count = fields.IntegerField
    overall_sentiment = fields.IntegerField
    created_at = fields.DateTimeField
    updated_at = fields.DateTimeField
