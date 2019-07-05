import redis
import requests

from yaml import safe_load
from yaml.scanner import ScannerError
from config import get_settings
from flask import request, Blueprint
from flask_restful import Api, Resource, url_for
from schemas.repository import JobSchema, JobInstructionsSchema
from marshmallow.exceptions import ValidationError
from models import db, Job, JobInstructions

dock_bp = Blueprint('dock', __name__)
api = Api(dock_bp)
settings = get_settings()

redis = redis.Redis(
            host=settings.REDIS_CONNECTION_URL,
            port=settings.REDIS_CONNECTION_PORT
        )

class Dock(Resource):
    def _get_job_key(self, jid):
        return ":".join([settings.JOB_PREFIX, f"v{settings.JOB_VERSION}", jid])

    def _grab_instructions(self, job):
        payload = {
            "repository": job.repository.name,
            "provider": job.repository.provider,
            "owner": str(job.repository.owner),
            "file_path": job.repository.file_path,
            "is_organization": job.repository.is_organization
        }

        response = requests.get(settings.AUTH_FILE_ENDPOINT, json=payload)

        if response.status_code >= 400:
            return None

        data = response.json()
        content = data.get('content')

        try:
            return safe_load(content)
        except ScannerError:
            return None

    def _create_job(self, rid):
        schema = JobSchema()
        i_schema = JobInstructionsSchema()
        job_payload = {
            "repository_id": rid
        }

        job = schema.load(job_payload)

        db.session.add(job)
        db.session.commit()

        instructions = self._grab_instructions(job)

        instruction_payload = {
            "job_id": job.id,
            "instructions": instructions
        }

        if not instructions:
            return {"Error": "Failed to grab instructions"}, 400

        i_job = i_schema.load(instruction_payload)

        db.session.add(i_job)
        db.session.commit()

        payload = schema.dump(job)
        payload["instruction_set"] = i_schema.dump(i_job)

        # Add to the redis database for the job workers to pickup
        redis.set(self._get_job_key(str(job.id)), str(payload))

        return payload, 201

    def post(self, rid):
        try:
            job = self._create_job(rid)
            if job:
                return job
        except ValidationError as e:
            return e.messages, 400

        return {}, 400

api.add_resource(Dock, '/repo/<rid>/job')
