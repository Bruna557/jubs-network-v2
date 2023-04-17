import datetime
import hashlib
import jwt

from app.settings import APP_SETTINGS


def get_encoded_jwt(username):
    return jwt.encode({"user": username}, APP_SETTINGS["SECRET_KEY"], "HS256",
                      {"exp": datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(hours=24))})


def hash_password(password):
    hash_object = hashlib.sha1(bytes(password, "utf-8"))
    return hash_object.hexdigest()
