import datetime
from flask import request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify, json
from sqlalchemy import and_

from Lib.tokenize import String


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('dev_config.py', silent=True)
    from Scripts.activityfeed.app.models import db
    db.init_app(app)
    migrate = Migrate(app, db)

    from Scripts.activityfeed.app import views

    app.register_blueprint(views.bp)

    return app

