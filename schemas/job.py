from marshmallow import Schema, post_load, validates, fields, EXCLUDE
from models import Job

class CommitAuthor(Schema):
    author = fields.Str()

    class Meta:
        unknown = EXCLUDE

class Repository(Schema):
    id = fields.Number()
    full_name = fields.Str()
    private = fields.Bool()

    class Meta:
        unknown = EXCLUDE

class CommitSchema(Schema):
    ref = fields.Str()
    message = fields.Str()
    time = fields.DateTime()
    url = fields.Url()
    author = fields.Nested(CommitAuthor)
    repository = fields.Nested(Repository)
    added = fields.List(fields.Str())
    removed = fields.List(fields.Str())
    modified = fields.List(fields.Str())

    class Meta:
        unknown = EXCLUDE
