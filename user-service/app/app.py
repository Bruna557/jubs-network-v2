from bson import json_util
from flask import Flask, request, Response
import logging

from app import database as db
from app import publisher


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/users/<username>", methods=["GET"])
def get_user(username):
    user = {}

    try:
        logging.info("Connecting to MongoDB")
        jubs_db = db.mongo_connection()

        logging.info("Fetching user")
        user = jubs_db.users.find_one({"username": username})
        response = Response(json_util.dumps(user))
        response.headers["Cache-Control"] = "public, max-age=60"

    except Exception as e:
        logging.error(f"Failed to fetch user: {e}")
        response = Response(json_util.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    response.status = 200
    return response


@app.route("/users", methods=["POST"])
def create_user():
    try:
        logging.info("Connecting to MongoDB")
        jubs_db = db.mongo_connection()

        logging.info("Adding user")
        data = request.get_json()
        jubs_db.users.insert_one({"username": data["username"], "password": data["password"], "bio": data["bio"],
                                  "picture": data["picture"]})
        return "OK"

    except Exception as e:
        logging.error(f"Failed to create user: {e}")
        response = Response(json_util.dumps({"error": str(e)}))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/users/<username>", methods=["PUT"])
def edit_user(username):
    try:
        logging.info("Connecting to MongoDB")
        jubs_db = db.mongo_connection()

        if password := request.get_json()["password"]:
            logging.info("Updating password")
            jubs_db.users.update_one({"username": username}, {"$set": {"password": password}})
        if bio := request.get_json()["bio"]:
            logging.info("Updating bio")
            jubs_db.users.update_one({"username": username}, {"$set": {"bio": bio}})
        if picture := request.get_json()["picture"]:
            logging.info("Updating picture")
            jubs_db.users.update_one({"username": username}, {"$set": {"picture": picture}})
        return "OK"

    except Exception as e:
        logging.error(f"Failed to update user info: {e}")
        response = Response(json_util.dumps({"error": str(e)}))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/users/<username>", methods=["DELETE"])
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)
