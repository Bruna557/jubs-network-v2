from bson import json_util
from flask import Flask, Response
import logging

from . import database as db

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
