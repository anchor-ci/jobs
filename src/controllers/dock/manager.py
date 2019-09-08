import redis
import requests
import json

from yaml import safe_load
from yaml.scanner import ScannerError
from config import get_settings
from schemas.repository import JobSchema, JobInstructionsSchema
from schemas.job import JobHistorySchema
from models import db, Job, JobInstructions
from controllers.dock.runner import JobConstructor

class DockManager:
    def __init__(self):
        self.settings = get_settings()
        self.redis = redis.Redis(
            host=self.settings.REDIS_CONNECTION_URL,
            port=self.settings.REDIS_CONNECTION_PORT
        )

    def _get_job_key(self, jid):
        return ":".join([self.settings.JOB_PREFIX, f"v{self.settings.JOB_VERSION}", jid])

    def _normalize_job_file(self, content):
        """
        This function takes in a string in the follow formats:
            - YAML
            - JSON
            - TOML
            - XML

        And returns a Python Dictionary.

        NOTE: For now it just accepts YAML
        """
        normalized_content = None

        try:
            normalized_content = safe_load(content)
        except ScannerError:
            pass

        return normalized_content

    def _grab_instructions(self, job):
        """
        Grab instructions should retrieve the job from a location
        and normalize it into a Python dictionary, to be passed off
        onto a JobConstructor
        """
        payload = {
            "repository": job.repository.name,
            "provider": job.repository.provider,
            "owner": str(job.repository.owner),
            "file_path": job.repository.file_path,
            "is_organization": job.repository.is_organization
        }

        response = requests.get(self.settings.AUTH_FILE_ENDPOINT, json=payload)

        if response.status_code >= 400:
            return None

        data = response.json()
        content = data.get('content')
        content = self._normalize_job_file(content)

        return content

    def create_job(self, rid):
        schema = JobSchema()
        historySchema = JobHistorySchema()
        i_schema = JobInstructionsSchema()

        job_payload = {
            "repository_id": rid
        }

        job = schema.load(job_payload)

        db.session.add(job)
        db.session.commit()

        instructions = self._grab_instructions(job)

        constructor = JobConstructor(instructions)
        transformed_instructions = constructor.create()

        instruction_payload = {
            "job_id": job.id,
            "instructions": transformed_instructions
        }

        print(instruction_payload)

        if not instructions:
            return {"Error": "Failed to grab instructions"}, 400

        i_job = i_schema.load(instruction_payload)
        history = self._create_history(job.id)

        db.session.add(i_job)
        db.session.add(history)

        # Don't commit until after history is made and added
        db.session.commit()

        payload = schema.dump(job)
        payload["instruction_set"] = i_schema.dump(i_job)
        payload["history"] = historySchema.dump(history)

        # Add to the redis database for the job workers to pickup
        self.redis.set(
            self._get_job_key(str(job.id)),
            json.dumps(payload)
        )

        return payload, 201

    def _create_history(self, jid):
        schema = JobHistorySchema()
        data = schema.load({"job_id": jid})
        return data
