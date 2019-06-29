from marshmallow import Schema, fields, post_load, validates, validate
from marshmallow.exceptions import ValidationError
from sqlalchemy import exists
from models import Repository, Job, db, JobInstructions

PROVIDERS = (
    "github",
    "gitlab"
)

class JobSchema(Schema):
    id = fields.UUID(dump_only=True)
    state = fields.Str(dump_only=True)
    repository_id = fields.UUID(required=True)

    @validates('repository_id')
    def validate_rid(self, data, **kwargs):
        result = db.session.query(exists().where(Repository.id == data)).scalar()
        if not result:
            raise ValidationError(f"Repository {data} does not exist")

    @post_load
    def create_job(self, data, **kwargs):
        return Job(**data)

class JobInstructionsSchema(Schema):
    id = fields.UUID(dump_only=True)
    job_id = fields.UUID()
    instructions = fields.List(fields.Str())

    @post_load
    def create_job_instructions(self, data, **kwargs):
        return JobInstructions(**data)

class RepositorySchema(Schema):
    id = fields.UUID()
    provider = fields.Str()
    name = fields.Str()
    file_path = fields.Str(required=False)

class GetRepositoryRequest(Schema):
    rid = fields.UUID()
    jobs = fields.Nested(JobSchema, many=True, dump_only=True)

    @validates('rid')
    def validate_rid(self, data, **kwargs):
        result = db.session.query(exists().where(Repository.id == data)).scalar()
        if not result:
            raise ValidationError(f"Repository {data} does not exist")

class PostRepositoryRequest(Schema):
    provider = fields.Str(required=True, validate=validate.OneOf(PROVIDERS))
    name = fields.Str(required=True)

    @post_load
    def load_repo(self, data, **kwargs):
        return Repository(**data)
