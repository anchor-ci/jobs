from marshmallow import Schema, post_load, validates, fields, EXCLUDE
from models import Job, JobHistory
from schemas.repository import JobSchema

class JobHistorySchema(Schema):
    id = fields.UUID(dump_only=True)
    job_id = fields.UUID(load_only=True)
    history = fields.List(fields.Dict())

    @post_load
    def create_history(self, data, **kwargs):
        return JobHistory(**data)
