from flask import request, Blueprint
from flask_restful import Api, Resource, url_for
from marshmallow.exceptions import ValidationError
from models import db, Job, JobInstructions, Repository, JobHistory
from config import get_settings
from schemas.repository import JobSchema, JobInstructionsSchema
from schemas.job import JobHistorySchema
from schemas.request_schemas import HistoryUpdateSchema, JobUpdateSchema
from queries import (
    get_job_history,
    job_history_exists,
    get_job_history_condition,
    get_job,
    job_exists,
    get_job_condition
)

job = Blueprint('job', __name__)
api = Api(job)
settings = get_settings()

class StatsController(Resource):
    def get(self, rid):
        return {}

class HistoryController(Resource):
    def _get_one(self, hid):
        schema = JobHistorySchema()
        data = get_job_history(hid)

        if not data:
            return {}, 404

        return schema.dump(data), 200

    def get(self, hid=None):
        """
        GET is used to grab the entire history by job id
        """
        if not hid:
            return None, 400

        try:
            response = self._get_one(hid)
        except ValidationError as e:
            response = e.messages, 400

        return response

    def put(self, hid=None):
        """
        PUT is used to update a line in the actual history itself
        """
        if request.json == None or not request.json or not hid:
            return None, 400

        schema = HistoryUpdateSchema()
        payload = {**request.json, **{"id": hid}}
        response = {}, 200

        try:
            data = schema.load(payload)

            if not job_history_exists(hid):
                return {"error": f"{hid} doesn't exist"}, 400

            history = get_job_history(hid)
            history.history = [*history.history, *data.get("history", [])]

            db.session.commit()

            response = {}, 204
        except ValidationError as e:
            response = e.messages, 400

        return response

class JobHistoryController(Resource):
    def _get_one(self, hid):
        schema = JobHistorySchema()
        data = get_job_history(hid)
        return schema.dump(data), 200

    def _get_all(self):
        return [], 404

    def get(self, jid, hid=None):
        """
        GET is used to grab the entire history by job id
        """
        try:
            if hid:
                response = self._get_one(hid)
            else:
                response = self._get_all(jid)
        except ValidationError as e:
            response = e.messages, 400

        return response

    def post(self, jid, hid=None):
        """
        POST is used to create part of the job history
        """
        if request.json == None:
            return None, 400

        schema = JobHistorySchema()
        payload = {**request.json, **{"job_id": jid}}
        response = {}, 200

        try:
            data = schema.load(payload)

            db.session.add(data)
            db.session.commit()

            response = schema.dump(data), 201
        except ValidationError as e:
            response = e.messages, 400

        return response

    def put(self, jid, hid=None):
        """
        PUT is used to update a line in the actual history itself
        """
        if request.json == None:
            return None, 400

        schema = HistoryUpdateSchema()
        payload = {**request.json, **{"job_id": jid, "id": hid}}
        response = {}, 200

        try:
            data = schema.load(payload)

            if not job_history_exists(hid):
                return {"error": f"{hid} doesn't exist"}, 400

            history = get_job_history_condition(JobHistory.id == hid)
            history.update(data)

            db.session.commit()

            response = {}, 204
        except ValidationError as e:
            response = e.messages, 400

        return response

class RepositoryJobController(Resource):
    def _get_one(self, rid, jid):
        schema = JobSchema()
        job = get_job(jid)
        return schema.dump(job)

    def _get_all(self, rid):
        schema = JobSchema(many=True)
        jobs = Job.query.filter(Job.repository_id == rid).order_by(Job.created_at.desc()).all()
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

class JobController(Resource):
    def _get_one(self, jid):
        schema = JobSchema()
        item = get_job(jid)
        return schema.dump(item)

    def get(self, jid=None):
        if not jid:
            return {}, 400

        response = {}, 200

        try:
            if jid:
                response = self._get_one(jid), 200
        except ValidationError as e:
            response = e.messages, 400

        if not response[0]:
            response = response[0], 400

        return response

    def put(self, jid):
        if request.json == None or not request.json:
            return None, 400

        schema = JobUpdateSchema()
        payload = {**request.json, **{"id": jid}}
        response = {}, 200

        try:
            data = schema.load(payload)

            if not job_exists(jid):
                return {"error": f"{jid} doesn't exist"}, 400

            job = get_job_condition(Job.id == jid)
            job.update(data)

            db.session.commit()

            response = {}, 204
        except ValidationError as e:
            response = e.messages, 400

        return response

#TODO: Move stats controller to repository
api.add_resource(StatsController, '/stats/<rid>')
api.add_resource(HistoryController, '/histories/<hid>')
api.add_resource(JobController, '/jobs/<jid>')
api.add_resource(JobHistoryController, '/history/<jid>', '/history/<jid>/<hid>')
api.add_resource(RepositoryJobController, '/job/<rid>', '/job/<rid>/<jid>')
