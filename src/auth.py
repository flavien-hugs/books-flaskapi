from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

import validators
from src.database import db, User
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
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

    if User.query.filter_by(user_addr_email=user_addr_email).one_or_none() is not None:
        return jsonify({"error": "Email is taken"}), HTTP_409_CONFLICT

    if User.query.filter_by(user_fullname=user_fullname).one_or_none() is not None:
        return jsonify({"error": "Username is taken"}), HTTP_409_CONFLICT

    password_hashed = generate_password_hash(user_password)
    new_user = User(
        user_fullname=user_fullname,
        user_addr_email=user_addr_email,
        user_password=password_hashed,
    )
    db.session.add(new_user)
    db.session.commit()

    data = {
        "user_fullname": user_fullname,
        "user_addr_email": user_addr_email,
    }

    return (
        jsonify({"message": "New user created successfully", "user": data}),
        HTTP_201_CREATED,
    )


@auth.post("/login", strict_slashes=False)
def login():
    user_addr_email = request.json.get("user_addr_email", None)
    user_password = request.json.get("user_password", None)

    user = User.query.filter_by(user_addr_email=user_addr_email).one_or_none()

    if user and check_password_hash(user.user_password, user_password):
        refresh_token = create_refresh_token(identity=user.id)
        access_token = create_access_token(identity=user.id)

        data = {
            "refresh_token": refresh_token,
            "access_token": access_token,
            "user_fullname": user.user_fullname,
            "user_email": user.user_addr_email,
        }

        return (
            jsonify({"message": "User logged successfully", "user": data}),
            HTTP_200_OK,
        )

    return jsonify({"error": "Wrong credentials"}), HTTP_401_UNAUTHORIZED


@auth.get("/me", strict_slashes=False)
@jwt_required()
def me():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).one_or_none()
    data = {
        "user_fullname": user.user_fullname,
        "user_addr_email": user.user_addr_email,
    }
    return jsonify({"user": data}), HTTP_200_OK


@auth.get("/token/refresh", strict_slashes=False)
@jwt_required(refresh=True)
def refresh_user_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    data = {"access_token": access_token}
    return jsonify({"access_token": data}), HTTP_200_OK
