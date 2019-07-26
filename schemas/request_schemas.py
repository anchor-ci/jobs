from marshmallow import Schema, fields, post_load, validates, validate, validates_schema
from marshmallow.exceptions import ValidationError

class HistoryAddSchema(Schema):
    job_id = fields.UUID(required=True, load_only=True)
    history_id = fields.UUID(required=True, load_only=True)
    update = fields.Dict(required=True)
