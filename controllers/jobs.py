from flask import request, Blueprint
from flask_restful import Api, Resource, url_for
from marshmallow.exceptions import ValidationError
from models import db, Job, JobInstructions, Repository, JobHistory
from config import get_settings
from schemas.repository import JobSchema, JobInstructionsSchema
from schemas.job import JobHistorySchema
from schemas.request_schemas import HistoryAddSchema

job = Blueprint('job', __name__)
api = Api(job)
settings = get_settings()

class JobHistoryController(Resource):
    def _get_one(self, hid):
        pass

    def _get_all(self):
        pass

    def get(self, jid):
        """
        GET is used to grab the entire history by job id
        """
        pass

    def post(self, jid, hid=None):
        """
        POST is used to create part of the job history
        """
        if request.json == None:
            return None, 400

        schema = JobHistorySchema()
        payload = {**request.json, **{"job_id": jid, "history_id": hid}}
        response = {}, 200

        try:
            data = schema.load(payload)

            db.session.add(data)
            db.session.commit()

            response = schema.dump(data), 200
        except ValidationError as e:
            response = e.messages, 400

        return response

    def put(self, jid, hid=None):
        """
        PUT is used to update a line in the actual history itself
        """
        if request.json == None:
            return None, 400

        schema = HistoryAddSchema()
        payload = {**request.json, **{"job_id": jid, "history_id": hid}}
        response = {}, 200

        try:
            data = schema.load(payload)

            print(data)

            response = data, 200
        except ValidationError as e:
            response = e.messages, 400

        return response

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

api.add_resource(JobHistoryController, '/history/<jid>', '/history/<jid>/<hid>')
api.add_resource(JobController, '/job/<rid>', '/job/<rid>/<jid>')
