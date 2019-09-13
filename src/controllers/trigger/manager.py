from models import db, WebhookTrigger
from schemas.trigger import WebhookTriggerSchema
from queries import get_repository

class WebhookTriggerManager:
    def grab(self, tid):
        schema = WebhookTriggerSchema()
        entry = schema.load({"id": tid})
        row = WebhookTrigger.query.get(tid)
        return schema.dump(row), 200

    def create(self, body):
        schema = WebhookTriggerSchema()
        entry = schema.load(body)
        row = WebhookTrigger(**entry)

        db.session.add(row)
        db.session.commit()

        return schema.dump(row), 201

    def update(self, body):
        schema = WebhookTriggerSchema()
        entry = schema.load(body)

        repository = get_repository(**entry)

        print(repository)

        return {}
