import requests

from config import get_settings
from controllers.images import images
from controllers.jobs import job
from controllers.repository import repo_bp
from controllers.dock.dock import dock_bp
from controllers.trigger.triggers import triggers
from models import db, JobInstructions, Repository, Job
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

def get_app(config=get_settings()):
    app = Flask(__name__)
    app.config.from_object(config)

    apply_settings(app)
    register_extensions(app)
    register_blueprints(app)

    return app

def register_blueprints(app):
    app.register_blueprint(triggers, url_prefix='/triggers')
    app.register_blueprint(repo_bp)
    app.register_blueprint(dock_bp)
    app.register_blueprint(job)
    app.register_blueprint(images, url_prefix="/images")

def apply_settings(app):
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

def register_extensions(app):
    db.init_app(app)

    with app.app_context():
        # TODO: Remove before prod deployment ;D
        db.create_all()
        db.session.commit()

application = get_app()

CORS(application, origins="*", allow_headers=["Content-Type", "Access-Control-Allow-Credentials"])

if __name__ == '__main__':
    application.run(debug=True, host="0.0.0.0", port=8080)

