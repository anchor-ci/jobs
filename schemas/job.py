from marshmallow import Schema, post_load, validates, fields, EXCLUDE
from models import Job, JobHistory
from schemas.repository import JobSchema

class JobHistorySchema(Schema):
    job_id = fields.UUID(load_only=True)
    history = fields.List(fields.Dict())
    job = fields.Nested(JobSchema, dump_only=True)

    @post_load
    def create_history(self, data, **kwargs):
        return JobHistory(**data)
