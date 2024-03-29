from marshmallow import Schema, fields, post_load, validates, validate, validates_schema
from marshmallow.exceptions import ValidationError
from sqlalchemy import exists
from models import Repository, Job, db, JobInstructions

PROVIDERS = (
    "github",
    "gitlab"
)

class JobInstructionsSchema(Schema):
    id = fields.UUID(dump_only=True)
    job_id = fields.UUID(load_only=True)
    instructions = fields.Dict()

    @post_load
    def create_job_instructions(self, data, **kwargs):
        return JobInstructions(**data)

class RepositorySchema(Schema):
    id = fields.UUID(dump_only=True)
    owner = fields.UUID(required=True)
    provider = fields.Str(required=True, validate=validate.OneOf(PROVIDERS))
    name = fields.Str(required=True)
    file_path = fields.Str()
    is_organization = fields.Bool(default=False)

    @validates('owner')
    def validate_user(self, data, **kwargs):
        # TODO: Finish this
        pass

    @validates_schema
    def validate_name(self, data, **kwargs):
        name = data.get('name')
        owner = data.get('owner')

        result = db.session.query(exists().where(Repository.owner == owner).where(Repository.name == name)).scalar()
        if result:
            raise ValidationError(f"Repository named {name} with owner {owner} already exists!")

    @post_load
    def load_repo(self, data, **kwargs):
        return Repository(**data)

class JobSchema(Schema):
    id = fields.UUID(dump_only=True)
    state = fields.Str(dump_only=True)
    repository_id = fields.UUID(required=True, load_only=True)
    repository = fields.Nested(RepositorySchema)
    created_at = fields.DateTime()

    @validates('repository_id')
    def validate_rid(self, data, **kwargs):
        result = db.session.query(exists().where(Repository.id == data)).scalar()
        if not result:
            raise ValidationError(f"Repository {data} does not exist")

    @post_load
    def create_job(self, data, **kwargs):
        return Job(**data)

class GetUserRepositoryRequest(Schema):
    uuid = fields.UUID()

    @validates('uuid')
    def verify_user(self, data, **kwargs):
        # TODO: Verify the user exists
        pass

    @post_load
    def get_repo_by_user(self, data, **kwargs):
        return Repository.query.filter_by(
            owner=data.get('uuid')
        ).all()

class GetRepositoryRequest(Schema):
    rid = fields.UUID()
    jobs = fields.Nested(JobSchema, many=True, dump_only=True)

    @validates('rid')
    def validate_rid(self, data, **kwargs):
        result = db.session.query(exists().where(Repository.id == data)).scalar()
        if not result:
            raise ValidationError(f"Repository {data} does not exist")
