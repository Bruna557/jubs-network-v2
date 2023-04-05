from bson import json_util
from flask import Flask, request, Response
import logging

from . import database as db
from . import publisher

app = Flask(__name__)


@app.route("/users/<username>", methods=["GET"])
def get_user(username):
    user = {}

    try:
        logging.info("Connecting to MongoDB")
        jubs_db = db.mongo_connection()

        logging.info("Fetching user")
        user = jubs_db.users.find_one({ "username": username })

    except Exception as e:
        print(f"ERROR: {e}")

    response = Response(json_util.dumps(user))
    response.headers["Cache-Control"] = "public, max-age=60"
    response.headers["Content-Type"] = "application/json"
    response.status = 201
    return response


@app.route("/users", methods=["POST"])
def create_user():
    try:
        logging.info("Connecting to MongoDB")
        jubs_db = db.mongo_connection()

        logging.info("Adding user")
        data = request.get_json()
        jubs_db.users.insert_one({ "username": data["username"],
                                   "password": data["password"],
                                   "bio": data["bio"],
                                   "picture": data["picture"] })

    except Exception as e:
        print(f"ERROR: {e}")

    return "OK"


@app.route("/users/change-password/<username>", methods=["PUT"])
def change_password(username):
    try:
        logging.info("Connecting to MongoDB")
        jubs_db = db.mongo_connection()

        logging.info("Updating password")
        jubs_db.users.update_one({ "username": username }, { "$set": { "password":  request.get_json()["password"]} })

    except Exception as e:
        print(f"ERROR: {e}")

    return "OK"


@app.route("/users/change-bio/<username>", methods=["PUT"])
def change_bio(username):
    try:
        logging.info("Connecting to MongoDB")
        jubs_db = db.mongo_connection()

        logging.info("Updating bio")
        jubs_db.users.update_one({ "username": username }, { "$set": { "bio":  request.get_json()["bio"]} })

    except Exception as e:
        print(f"ERROR: {e}")

    return "OK"


@app.route("/users/change-picture/<username>", methods=["PUT"])
def change_picture(username):
    try:
        logging.info("Connecting to MongoDB")
        jubs_db = db.mongo_connection()

        logging.info("Updating picture")
        jubs_db.users.update_one({ "username": username }, { "$set": { "picture":  request.get_json()["picture"]} })

    except Exception as e:
        print(f"ERROR: {e}")

    return "OK"


@app.route("/users/<username>", methods=["DELETE"])
def delete_user(username):
    try:
        logging.info("Connecting to MongoDB")
        jubs_db = db.mongo_connection()

        logging.info("Deleting user")
        jubs_db.users.delete_one({ "username": username })
        publisher.publish_user_deleted_event(username)

    except Exception as e:
        print(f"ERROR: {e}")

    return "OK"
