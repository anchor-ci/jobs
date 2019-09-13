from marshmallow import Schema, fields
from schemas.repository import RepositorySchema

class WebhookTriggerSchema(Schema):
    id = fields.UUID()
    name = fields.Str(required=True)
    repository_id = fields.UUID(required=True)
    repository = fields.Nested(RepositorySchema)
