from flask_restful import Resource, Api
from flask import Blueprint, request
from marshmallow.exceptions import ValidationError
from controllers.trigger.manager import WebhookTriggerManager

triggers = Blueprint('triggers', __name__)
api = Api(triggers)

class WebhookTriggerController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.manager = WebhookTriggerManager()

    def _get_one(self, tid):
        pass

    def _get_all(self):
        pass

    def get(self, tid=None):
        try:
            return self.manager.grab(tid)
        except ValidationError as e:
            return e.messages, 400

        return {}, 400

    def post(self, tid=None):
        try:
            return self.manager.create(request.json)
        except ValidationError as e:
            return e.messages, 400

        return {}, 400

    def delete(self, tid=None):
        pass

    def put(self, tid=None):
        try:
            return self.manager.update(request.json)
        except ValidationError as e:
            return e.messages, 400

        return {}, 400

api.add_resource(WebhookTriggerController, '/webhook', '/webhook/<tid>')
