import os

from flask import Flask

from src.auth import auth
from src.books import books


def create_app(config_name=None):

    app = Flask(__name__, instance_relative_config=True)

    if config_name is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
        )
    else:
        app.config.from_mapping(config_name)

    app.register_blueprint(auth)
    app.register_blueprint(books)

    return app
