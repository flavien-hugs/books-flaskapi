from flask import Blueprint

books = Blueprint("books", __name__, url_prefix="/api/v1/books")


@books.get("/")
def get_all():
    return {"books": "[]"}
