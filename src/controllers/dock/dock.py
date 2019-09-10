from flask import request, Blueprint
from flask_restful import Api, Resource, url_for
from marshmallow.exceptions import ValidationError
from controllers.dock.manager import DockManager

dock_bp = Blueprint('dock', __name__)
api = Api(dock_bp)

class Dock(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.manager = DockManager()

    def post(self, trigger_id):
        try:
            job = self.manager.create_job(rid)
            if job:
                return job
        except ValidationError as e:
            return e.messages, 400

        return {}, 400

api.add_resource(Dock, '/repo/<trigger_id>/job')
