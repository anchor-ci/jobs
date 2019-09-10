import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB, JSON
from uuid import uuid4
from config import get_settings

settings = get_settings()
db = SQLAlchemy()

VALID_STATES = (
    "STARTING",
    "RUNNING",
    "SUCCESS",
    "FAILED",
    "TERMINATED"
)

class Repository(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4)
    # Can be a uuid pointing at an organization or a user_id
    owner = db.Column(UUID(as_uuid=True))
    provider = db.Column(db.String(127), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False, default=settings.DEFAULT_CI_FILE)
    # This field indicates if the owner field is an organization or not
    is_organization = db.Column(db.Boolean(), unique=False, default=False)

    def __init__(self, provider, name, owner, is_organization=False):
        self.is_organization = is_organization
        self.provider = provider
        self.name = name
        self.owner = owner

class Job(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4)
    state = db.Column(db.String(127), nullable=False)
    repository_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Repository.id))
    repository = db.relationship(Repository, cascade="all,delete")
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, repository_id):
        repo = Repository.query.filter_by(id=repository_id).first()

        self.repository_id = repository_id
        self.repository = repo
        self.state = "STARTING"

    def __repr__(self):
        return f"<{self.repository} | {self.state}>"

class JobInstructions(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4)
    job_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Job.id))
    job = db.relationship(Job, cascade="all,delete")
    instructions = db.Column(JSONB)

    def __init__(self, instructions, job_id=None, job=None):
        if not any((job_id, job)):
            raise ValueError("Must specify a job id, or a job")

        linked_job = job
        if job_id:
            linked_job = Job.query.filter_by(id=job_id).first()

        self.job_id = linked_job.id
        self.job = linked_job
        self.instructions = instructions

class JobHistory(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4)
    job_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Job.id))
    job = db.relationship(Job, cascade="all,delete")
    history = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, history=[], job_id=None, job=None):
        if not any((job_id, job)):
            raise ValueError("Must specify a job id, or a job")

        linked_job = job
        if job_id:
            linked_job = Job.query.filter_by(id=job_id).first()

        self.job_id = linked_job.id
        self.job = linked_job
        self.history = history

class WebhookTrigger(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4)
    repository_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Repository.id), nullable=True)
    repository = db.relationship(Repository)

    def __init__(self, repository_id=None):
        if repository_id:
            self.repository_id = repository_id
            self.repository = Repository.query.filter_by(id=repository_id).first()

