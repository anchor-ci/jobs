import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from uuid import uuid4
from config import get_settings

settings = get_settings()
db = SQLAlchemy()

class Repository(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4)
    user_id = db.Column(UUID(as_uuid=True), unique=True)
    provider = db.Column(db.String(127), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False, default=settings.DEFAULT_CI_FILE)

    def __init__(self, provider, name, user_id):
        self.provider = provider
        self.name = name
        self.user_id = user_id

class Job(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4)
    state = db.Column(db.String(127), nullable=False)
    repository_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Repository.id))
    repository = db.relationship(Repository, cascade="all,delete")

    def __init__(self, repository_id):
        repo = Repository.query.filter_by(id=repository_id).first()

        self.repository_id = repository_id
        self.repository = repo
        self.state = "STARTING"

    def __repr__(self):
        return f"<{self.repository_id}: {self.repository} | {self.state}>"

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
