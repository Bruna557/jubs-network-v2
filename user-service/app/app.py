from bson import json_util
from flask import Flask, request, Response
import jwt
import logging

from app import database as db
from app import publisher
from app.auth import is_authorized
from app.settings import APP_SETTINGS
from app.utils import get_encoded_jwt, hash_password


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/users/<_username>", methods=["GET"])
@is_authorized
def get_user(_username):
    try:
        logging.info("Connecting to MongoDB")
        jubs_db = db.mongo_connection()

        logging.info("Fetching user")
        user = jubs_db.users.find_one({"username": _username}, {"username": 1, "bio": 1, "picture": 1, "_id": 0})
        response = Response(json_util.dumps(user))
        response.headers["Cache-Control"] = "public, max-age=60"
        response.status = 200

    except Exception as e:
        logging.error(f"Failed to fetch user: {e}")
        response = Response(json_util.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/users", methods=["GET"])
@is_authorized
def search_users():
    try:
        logging.info("Connecting to MongoDB")
        jubs_db = db.mongo_connection()

        logging.info("Searching users")
        starts_with = request.args.get("username")
        users = jubs_db.users.find({"username":{"$regex":f"^{starts_with}"}},
                                   {"username": 1, "bio": 1, "picture": 1, "_id": 0})
        response = Response(json_util.dumps(users))
        response.headers["Cache-Control"] = "public, max-age=60"
        response.status = 200

    except Exception as e:
        logging.error(f"Failed to search users: {e}")
        response = Response(json_util.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/users", methods=["POST"])
def create_user():
    try:
        logging.info("Connecting to MongoDB")
        jubs_db = db.mongo_connection()

        logging.info("Adding user")
        data = request.get_json()
        hashed_password = hash_password(data["password"])
        jubs_db.users.insert_one({"username": data["username"], "password": hashed_password, "bio": data["bio"],
                                  "picture": data["picture"]})
        encoded_jwt = get_encoded_jwt(data["username"])
        response = Response(json_util.dumps({"token": encoded_jwt}))
        response.status = 200

    except Exception as e:
        logging.error(f"Failed to create user: {e}")
        response = Response(json_util.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/users/<username>", methods=["PUT"])
@is_authorized
def edit_user(username):
    try:
        logging.info("Connecting to MongoDB")
        jubs_db = db.mongo_connection()

        data = request.get_json()

        if "password" in data:
            logging.info("Updating password")
            hashed_password = hash_password(data["password"])
            jubs_db.users.update_one({"username": username}, {"$set": {"password": hashed_password}})
            data["password"] = "REDACTED"
        if "bio" in data:
            logging.info("Updating bio")
            jubs_db.users.update_one({"username": username}, {"$set": {"bio": data["bio"]}})
        if "picture" in data:
            logging.info("Updating picture")
            jubs_db.users.update_one({"username": username}, {"$set": {"picture": data["picture"]}})

        response = Response(json_util.dumps(data))
        response.status = 200

    except Exception as e:
        logging.error(f"Failed to update user info: {e}")
        response = Response(json_util.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/users/<username>", methods=["DELETE"])
@is_authorized
def delete_user(username):
    try:
        logging.info("Connecting to MongoDB")
        jubs_db = db.mongo_connection()

        logging.info("Deleting user")
        jubs_db.users.delete_one({"username": username})
        publisher.publish_user_deleted_event(username)
        return "OK"

    except Exception as e:
        logging.error(f"Failed to delete user: {e}")
        response = Response(json_util.dumps({"error": str(e)}))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        hashed_password = hash_password(password)

        logging.info("Connecting to MongoDB")
        jubs_db = db.mongo_connection()

        logging.info("Authenticating user")
        user = jubs_db.users.find_one({"username": username, "password": hashed_password})

        if not user:
            logging.error(f"Login failed: invalid credentials")
            response = Response(json_util.dumps({"error": "Invalid credentials"}))
            response.status = 401
        else:
            encoded_jwt = get_encoded_jwt(user["username"])
            response = Response(json_util.dumps({"token": encoded_jwt}))
            response.status = 200

    except Exception as e:
        logging.error(f"Failed to authenticate user: {e}")
        response = Response(json_util.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/auth/logout/<username>", methods=["DELETE"])
@is_authorized
def logout(username):
    try:
        authorization_header = request.headers.get("authorization")
        token = authorization_header.replace("Bearer ", "")

        logging.info("Connecting to MongoDB")
        jubs_db = db.mongo_connection()

        logging.info("Adding token to blacklist")
        jubs_db.blacklist.insert_one({"username": username, "token": token})

        return "OK"

    except Exception as e:
        logging.error(f"Failed to log out: {e}")
        response = Response(json_util.dumps({"error": str(e)}))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/auth/token/verify", methods=["POST"])
def verify_token():
    try:
        token = request.get_json()["token"]
        decoded = jwt.decode(token, APP_SETTINGS["SECRET_KEY"], algorithms=["HS256"])

        logging.info("Connecting to MongoDB")
        jubs_db = db.mongo_connection()

        blacklisted = jubs_db.blacklist.find({"username": decoded["user"]})

        for document in blacklisted:
            if token == document["token"]:
                raise Exception("Token is blacklisted")

        response = Response(json_util.dumps(decoded))
        response.status_code = 200

    except Exception as e:
        logging.error(f"Verification failed: {e}")
        response = Response(json_util.dumps({"error": str(e)}))
        response.status = 401

    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5008, debug=True)
