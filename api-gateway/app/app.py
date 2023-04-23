from datetime import datetime
from flask import abort, Flask, json, request, Response
from flask_cors import CORS
from functools import wraps
import logging

from app import database as redis
from app.repository import RedisRepository
from app.services import TimelineService, AuthService
from app import utils


app = Flask(__name__)
CORS(app, supports_credentials=True)
repository = RedisRepository(redis)
timeline_service = TimelineService(repository)
auth_service = AuthService(repository)
logging.basicConfig(level=logging.INFO)


def is_authorized(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        authorization_header = request.headers.get("authorization") or ""
        token = authorization_header.replace("Bearer ", "")

        if token and auth_service.verify(token, request.view_args.get("username")):
            return function(*args, **kwargs)
        return abort(401)

    return decorator


@app.route("/timeline/<username>", methods=["GET"])
@is_authorized
def get_timeline(username):
    posted_on = request.args.get("posted_on") or int(datetime.timestamp(datetime.now()))
    scroll = request.args.get("scroll") or "down"

    res, status_code = timeline_service.get(username, posted_on, scroll)

    response = Response(res)
    response.status = status_code
    response.headers["Content-Type"] = "application/json"
    if status_code == 200:
        response.headers["Cache-Control"] = "public, max-age=60"
    return response


@app.route("/auth/login", methods=["POST"])
def login():
    res, status_code = utils.login(request.get_json())

    response = Response(res)
    response.status = status_code
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/auth/logout/<username>", methods=["DELETE"])
@is_authorized
def logout(username):
    try:
        authorization_header = request.headers.get("authorization")
        token = authorization_header.replace("Bearer ", "")

        auth_service.blacklist(username, token)

        response = Response("OK")
        response.status_code = 200

    except Exception as e:
        logging.error(f"Failed to log out: {e}")
        response = Response(json.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/users", methods=["POST"])
def create_user():
    res, status_code = utils.create_user(request.get_json())

    response = Response(res)
    response.status = status_code
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/users/<username>", methods=["GET"])
@is_authorized
def get_user(username):
    res, status_code = utils.get_user(username)

    response = Response(res)
    response.status = status_code
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/users/<username>/search", methods=["GET"])
@is_authorized
def search_users(username):
    res, status_code = utils.search_users(username, request.args.get("q"), request.args.get("page_size"), request.args.get("page_number"))

    response = Response(res)
    response.status = status_code
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/users/<username>", methods=["PUT"])
@is_authorized
def edit_user(username):
    res, status_code = utils.edit_user(username, request.get_json())

    response = Response(res)
    response.status = status_code
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/followings/<username>", methods=["GET"])
@is_authorized
def get_followings(username):
    res, status_code = utils.get_followings(username, request.args.get("page_size"), request.args.get("page_number"))

    response = Response(res)
    response.status = status_code
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/followers/<username>", methods=["GET"])
@is_authorized
def get_followers(username):
    res, status_code = utils.get_followers(username, request.args.get("page_size"), request.args.get("page_number"))

    response = Response(res)
    response.status = status_code
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/followers/recommendation/<username>", methods=["GET"])
@is_authorized
def get_recommendation(username):
    res, status_code = utils.get_recommendation(username, request.args.get("page_size"),
                                                request.args.get("page_number"))

    response = Response(res)
    response.status = status_code
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/follow/<username>/<followed>", methods=["POST"])
@is_authorized
def follow(username, followed):
    res, status_code = utils.follow(username, followed)

    response = Response(res)
    response.status = status_code
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/follow/<username>/<followed>", methods=["DELETE"])
@is_authorized
def unfollow(username, followed):
    res, status_code = utils.unfollow(username, followed)

    response = Response(res)
    response.status = status_code
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/users/<username>", methods=["DELETE"])
@is_authorized
def delete_user(username):
    res, status_code = utils.delete_user(username)

    response = Response(res)
    response.status = status_code
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/posts/<username>", methods=["POST"])
@is_authorized
def create_post(username):
    res, status_code = utils.create_post(username, request.get_json())

    response = Response(res)
    response.status = status_code
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/posts/<username>/<posted_on>", methods=["PUT"])
@is_authorized
def edit_post(username, posted_on):
    res, status_code = utils.edit_post(username, posted_on, request.get_json())

    response = Response(res)
    response.status = status_code
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/likes/<posted_by>/<posted_on>", methods=["PUT"])
@is_authorized
def like_post(posted_by, posted_on):
    res, status_code = utils.like_post(posted_by, posted_on)

    response = Response(res)
    response.status = status_code
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/posts/<username>/<posted_on>", methods=["DELETE"])
@is_authorized
def delete_post(username, posted_on):
    res, status_code = utils.delete_post(username, posted_on)

    response = Response(res)
    response.status = status_code
    response.headers["Content-Type"] = "application/json"

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5007, debug=True)
