from flask import Blueprint

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register", strict_slashes=False)
def register():
    return "User created"


@auth.get("/me", strict_slashes=False)
def me():
    return {"user": "me"}
