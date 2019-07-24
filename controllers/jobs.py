from flask import request, Blueprint
from flask_restful import Api, Resource, url_for
from marshmallow.exceptions import ValidationError
from models import db, Job, JobInstructions, Repository
from config import get_settings
from schemas.repository import JobSchema, JobInstructionsSchema

job = Blueprint('job', __name__)
api = Api(job)
settings = get_settings()

class JobController(Resource):
    def _get_one(self, jid):
        schema = JobSchema()

    def _get_all(self, rid):
        schema = JobSchema(many=True)
        jobs = Job.query.filter(Job.repository_id == rid).all()
        loaded_jobs = schema.dump(jobs)
        return loaded_jobs

    def get(self, rid, jid=None):
        response = {}, 200

        try:
            if jid:
                response = self._get_one(rid, jid), 200
            else:
                response = self._get_all(rid), 200
        except ValidationError as e:
            response = e.messages, 400

        if not response[0]:
            response = response[0], 400

        return response

api.add_resource(JobController, '/job/<rid>', '/job/<rid>/<jid>')
