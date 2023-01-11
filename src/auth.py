from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

import validators
from src.database import db, User
from src.constants.http_status_codes import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
)

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

PASSWORD_LENGTH = 6
FULLNAME_LENGTH = 4


@auth.post("/register", strict_slashes=False)
def register():
    user_fullname = request.json["user_fullname"]
    user_addr_email = request.json["user_addr_email"]
    user_password = request.json["user_password"]

    if len(user_password) < PASSWORD_LENGTH:
        return jsonify({"error": "Password is too short"}), HTTP_400_BAD_REQUEST

    if len(user_fullname) < FULLNAME_LENGTH:
        return jsonify({"error": "User fullname is too short"}), HTTP_400_BAD_REQUEST

    if not validators.email(user_addr_email):
        return jsonify({"error": "Email is not valid"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(user_addr_email=user_addr_email).first() is not None:
        return jsonify({"error": "Email is taken"}), HTTP_409_CONFLICT

    if User.query.filter_by(user_fullname=user_fullname).first() is not None:
        return jsonify({"error": "Username is taken"}), HTTP_409_CONFLICT

    password_hashed = generate_password_hash(user_password)
    new_user = User(
        user_fullname=user_fullname,
        user_addr_email=user_addr_email,
        user_password=password_hashed,
    )
    db.session.add(new_user)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "New user created successfully",
                "user": {
                    "user_fullname": user_fullname,
                    "user_addr_email": user_addr_email,
                },
            }
        ),
        HTTP_201_CREATED,
    )


@auth.get("/me", strict_slashes=False)
def me():
    return {"user": "me"}
