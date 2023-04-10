from functools import wraps
from flask import json, request, abort
import requests


def is_authorized(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        authorization_header = request.headers.get("authorization") or ""
        token = authorization_header.replace("Bearer ", "")

        if token and verify_token(token, request.view_args["username"] if "username" in request.view_args else None):
            return function(*args, **kwargs)
        return abort(401)

    return decorator


def verify_token(token, user=None):
    response = requests.post("http://localhost:5008/auth/token/verify", data=json.dumps({"token": token}),
                             headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        if user:
            return json.loads(response.text)["user"] == user
        return True
    return False
