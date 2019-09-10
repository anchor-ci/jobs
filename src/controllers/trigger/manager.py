from models import db, WebhookTrigger
from schemas.trigger import WebhookTriggerSchema

class WebhookTriggerManager:
    def grab(self, tid):
        schema = WebhookTriggerSchema()
        row = WebhookTrigger.query.get(tid)
        return schema.dump(row)

    def create(self, body):
        schema = WebhookTriggerSchema()
        entry = schema.load(body)
        row = WebhookTrigger(**entry)

        db.session.add(row)
        db.session.commit()

        return schema.dump(row), 201
