import models

from models import db, Job

from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, url_for
from marshmallow.exceptions import ValidationError
from schemas.repository import (
    RepositorySchema,
    GetRepositoryRequest,
    GetUserRepositoryRequest
)

repo_bp = Blueprint('repository', __name__)
api = Api(repo_bp)

class UserRepository(Resource):
    def get(self, uuid):
        schema = GetUserRepositoryRequest()

        try:
            loaded = schema.load({"uuid": uuid})

            if not loaded:
                return {}, 404

            repo_schema = RepositorySchema(many=True)
            response = repo_schema.dump(loaded), 200
        except ValidationError as e:
            response = e.messages, 400

        return response

class Repository(Resource):
    def _get_id(self, rid):
        request_schema = GetRepositoryRequest()

        try:
            payload = {
                "rid": rid,
                "jobs": Job.query.filter_by(repository_id=rid).all()
            }

            result = request_schema.load(payload)
            if not result:
                response = {}, 404
            else:
                schema = RepositorySchema()
                result = schema.dump(result)
                response = result, 200
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

api.add_resource(Repository, '/repo', '/repo/<rid>')
api.add_resource(UserRepository, '/repo/user/<uuid>')
