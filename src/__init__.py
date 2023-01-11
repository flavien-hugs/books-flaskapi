import os
import json
from flask import Flask, redirect, jsonify, make_response

from src.auth import auth
from src.books import books
from src.database import db, Book

from flask_jwt_extended import JWTManager
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


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

    @app.get("/", strict_slashes=False)
    def books_all():
        books = Book.query.all()
        data = []
        for item in books:
            data.append(
                {
                    "id": item.id,
                    "book_author_name": item.book_author_name,
                    "book_title": item.book_title,
                    "book_short_desc": item.book_short_desc,
                    "book_cover": item.book_cover,
                    "book_isbn": item.book_isbn,
                    "book_number_of_page": item.book_number_of_page,
                    "book_url": item.book_url,
                    "book_short_url": item.book_short_url,
                    "book_viewed": item.book_viewed,
                    "book_added_at": item.book_added_at,
                    "book_updated_at": item.book_updated_at,
                }
            )
        return jsonify({"books": data}), HTTP_200_OK

    @app.get("/<string:book_short_url>")
    def redirect_to_short_url(book_short_url):
        book = Book.query.filter_by(book_short_url=book_short_url).first_or_404()

        if book:
            book.book_viewed += 1
            db.session.commit()
            return redirect(book.book_url)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"error": "Not Found"}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return (
            jsonify({"error": "Something went wrong, we are working on it"}),
            HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return app
