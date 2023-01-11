import os

from flask import Flask


def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=True)

    if config_name is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
        )
    else:
        app.config.from_mapping(config_name)

    @app.get("/")
    def homepage():
        return {"message": "Hello World"}

    return app
