import os

from flask import Flask

from src.auth import auth
from src.books import books
from src.database import db
from flask_jwt_extended import JWTManager


def create_app(config_name=None):

    app = Flask(__name__, instance_relative_config=True)

    if config_name is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
        )
    else:
        app.config.from_mapping(config_name)

    db.app = app
    db.init_app(app)

    # Setup the Flask-JWT-Extended extension
    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(books)

    return app
