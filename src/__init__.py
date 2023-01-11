import os

from flask import Flask, redirect

from src.auth import auth
from src.books import books
from src.database import db, Book
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

    @app.get("/<string:book_short_url>")
    def redirect_to_short_url(book_short_url):
        book = Book.query.filter_by(book_short_url=book_short_url).first_or_404()

        if book:
            book.book_viewed += 1
            db.session.commit()
            return redirect(book.book_url)

    return app
