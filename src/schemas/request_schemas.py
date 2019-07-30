from marshmallow import Schema, fields, post_load, validates, validate, validates_schema
from models import VALID_STATES
from marshmallow.exceptions import ValidationError

class HistoryUpdateSchema(Schema):
    job_id = fields.UUID(load_only=True)
    id = fields.UUID(required=True, load_only=True)
    history = fields.List(fields.Dict(required=True))

class JobUpdateSchema(Schema):
    id = fields.UUID(load_only=True)
    state = fields.Str(load_only=True, validate=validate.OneOf(VALID_STATES))
