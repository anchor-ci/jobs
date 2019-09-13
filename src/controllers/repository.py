import models

from models import db, Job

from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, url_for
from marshmallow.exceptions import ValidationError
from queries import get_latest_history_from_job
from schemas.job import JobHistorySchema
from utils import validate_uuid
from models import Repository
from schemas.repository import (
    RepositorySchema,
    GetRepositoryRequest,
    GetUserRepositoryRequest
)

repo_bp = Blueprint('repository', __name__)
api = Api(repo_bp)

@repo_bp.route("/latest/history/<jid>", methods=["GET"])
def get_latest_repo(jid):
    schema = JobHistorySchema()

    if not validate_uuid(jid, version=1):
        return jsonify({"error": "Invalid UUID"}), 400

    history = get_latest_history_from_job(jid)
    data = schema.dump(history)
    return jsonify(data), 200

class UserRepository(Resource):
    def get(self, uuid):
        schema = GetUserRepositoryRequest()

        try:
            loaded = schema.load({"uuid": uuid})
            repo_schema = RepositorySchema(many=True)
            response = repo_schema.dump(loaded), 200
        except ValidationError as e:
            response = e.messages, 400

        return response

class RepositoryController(Resource):
    def _get_id(self, rid):
        response = None

        try:
            repository = Repository.query.get(rid)

            if not repository:
                response = {}, 404
            else:
                schema = RepositorySchema()
                response = schema.dump(repository), 200
        except ValidationError as e:
            response = e.messages, 400

        return response

    def _get_all(self):
        schema = RepositorySchema(many=True)
        objects = models.Repository.query.all()
        results = schema.dump(objects)
        return results, 200

    def get(self, rid=None):
        result = None
        if rid:
            result = self._get_id(rid)
        else:
            result = self._get_all()

        return result

    def post(self, rid=None):
        schema = RepositorySchema()
        response = {}, 200

        try:
            result = schema.load(request.json)
            if result:
                db.session.add(result)
                db.session.commit()
            response = schema.dump(result), 200
        except ValidationError as e:
            response = e.messages, 400

        return response

    def put(self, rid=None):
        pass

    def delete(self, rid=None):
        pass

api.add_resource(RepositoryController, '/repo', '/repo/<rid>')
api.add_resource(UserRepository, '/repo/user/<uuid>')
