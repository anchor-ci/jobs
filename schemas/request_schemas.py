from marshmallow import Schema, fields, post_load, validates, validate, validates_schema
from marshmallow.exceptions import ValidationError

class HistoryUpdateSchema(Schema):
    job_id = fields.UUID(required=True, load_only=True)
    id = fields.UUID(required=True, load_only=True)
    history = fields.List(fields.Dict(required=True))
