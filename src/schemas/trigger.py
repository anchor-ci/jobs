from marshmallow import Schema, fields
from schemas.repository import RepositorySchema

class WebhookTriggerSchema(Schema):
    id = fields.UUID(dump_only=True)
    repository_id = fields.UUID(missing=None)
    repository = fields.Nested(RepositorySchema)
