from flask import Flask, json, request, Response
import logging

from app import repository
from app.auth import is_authorized


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/followings/<username>", methods=["GET"])
@is_authorized
def get_followings(username):
    try:
        followings = repository.get_followings(username, request.args.get("page_size"), request.args.get("page_number"))
        response = Response(json.dumps(followings))
        response.status = 200
        response.headers["Cache-Control"] = "public, max-age=60"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/followers/<username>", methods=["GET"])
@is_authorized
def get_followers(username):
    try:
        followers = repository.get_followers(username, request.args.get("page_size"), request.args.get("page_number"))
        response = Response(json.dumps(followers))
        response.status = 200
        response.headers["Cache-Control"] = "public, max-age=60"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/followers/recommendation/<username>", methods=["GET"])
@is_authorized
def get_recommendation(username):
    try:
        followers = repository.get_recommendation(username, request.args.get("page_size"), request.args.get("page_number"))
        response = Response(json.dumps(followers))
        response.status = 200
        response.headers["Cache-Control"] = "public, max-age=60"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/follow/<username>/<followed>", methods=["POST"])
@is_authorized
def follow(username, followed):
    try:
        repository.follow(username, followed)
        return "OK"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/follow/<username>/<followed>", methods=["DELETE"])
@is_authorized
def unfollow(username, followed):
    try:
        repository.unfollow(username, followed)
        return "OK"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
