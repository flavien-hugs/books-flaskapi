from flask import Blueprint, request, jsonify

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
)
from src.database import db, Book

books = Blueprint("books", __name__, url_prefix="/api/v1/books")


@books.route("/", methods=["GET", "POST"], strict_slashes=False)
@jwt_required()
def handle_books():

    current_user = get_jwt_identity()

    if request.method == "POST":
        book_author_name = request.get_json().get("book_author_name")
        book_title = request.get_json().get("book_title")
        book_short_desc = request.get_json().get("book_short_desc")
        book_cover = request.get_json().get("book_cover")
        book_isbn = request.get_json().get("book_isbn")
        book_number_of_page = request.get_json().get("book_number_of_page")

        if Book.query.filter_by(book_isbn=book_isbn).one_or_none():
            return jsonify({"error": "URL already exists"}), HTTP_409_CONFLICT

        new_book = Book(
            book_author_name=book_author_name,
            book_title=book_title,
            book_short_desc=book_short_desc,
            book_cover=book_cover,
            book_isbn=book_isbn,
            book_number_of_page=book_number_of_page,
            user_id=current_user,
        )
        db.session.add(new_book)
        db.session.commit()

        data = {
            "id": new_book.id,
            "book_author_name": new_book.book_author_name,
            "book_title": new_book.book_title,
            "book_short_desc": new_book.book_short_desc,
            "book_cover": new_book.book_cover,
            "book_isbn": new_book.book_isbn,
            "book_number_of_page": new_book.book_number_of_page,
            "book_url": new_book.book_url,
            "book_added_at": new_book.book_added_at,
            "book_updated_at": new_book.book_updated_at,
        }

        return (
            jsonify({"message": "New book created successfully", "book": data}),
            HTTP_201_CREATED,
        )
    else:
        books = Book.query.filter_by(user_id=current_user)
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
