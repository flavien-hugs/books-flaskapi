import string
import random
from enum import unique
from datetime import datetime

from slugify import slugify
from flask_sqlalchemy import SQLAlchemy
from .utils import Updateable

db = SQLAlchemy()


class User(Updateable, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, index=True, primary_key=True)
    user_fullname = db.Column(db.String(80), unique=True, nullable=False)
    user_addr_email = db.Column(db.String(100), unique=True, nullable=False)
    user_password = db.Column(db.String(80), nullable=False)
    user_joined_at = db.Column(db.DateTime, default=datetime.now())
    user_updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    books = db.relationship("Book", backref="user", lazy="dynamic")

    def __repr__(self) -> str:
        return "User>>> {self.user_fullname}"

    def __str__(self):
        return f"{self.user_fullname}, {self.user_addr_email}"


class Book(Updateable, db.Model):

    __tablename__ = "book"

    id = db.Column(db.Integer, index=True, primary_key=True)
    book_author_name = db.Column(db.String(120), nullable=False)
    book_title = db.Column(db.String(80), unique=True, nullable=False)
    book_short_desc = db.Column(db.Text(180), nullable=True)
    book_cover = db.Column(db.String(180), nullable=True)
    book_isbn = db.Column(db.Integer, unique=True, nullable=False)
    book_number_of_page = db.Column(db.Integer, nullable=False)
    book_url = db.Column(db.String(80), nullable=False, index=True, unique=True)
    book_short_url = db.Column(db.String(6), nullable=True)
    book_viewed = db.Column(db.Integer, default=0)
    book_added_at = db.Column(db.DateTime, default=datetime.now())
    book_updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.book_short_url = self._generate_short_url()

    def __repr__(self) -> str:
        return "Book>>> {self.book_title}"

    def __str__(self):
        return f"{self.book_author_name}, {self.book_title}, {self.book_isbn}"

    def _generate_short_url(self):

        chars = string.digits + string.ascii_letters
        random_chars = "".join(random.choices(chars, k=6))
        if self.query.filter_by(book_short_url=random_chars).first():
            self._generate_short_url()
        return random_chars

    @staticmethod
    def generate_book_slug(target, value, oldvalue, initiator):
        if value and (not target.book_url or value != oldvalue):
            target.book_url = slugify(value)


db.event.listen(Book.book_title, "set", Book.generate_book_slug, retval=False)
