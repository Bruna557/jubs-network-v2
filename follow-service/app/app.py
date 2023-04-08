from flask import Flask, json, Response
import logging

from app import repository

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/followings/<username>", methods=["GET"])
def get_followings(username):
    try:
        followings = repository.get_followings(username)
        response = Response(json.dumps(followings))
        response.status = 200
        response.headers["Cache-Control"] = "public, max-age=60"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/followers/<username>", methods=["GET"])
def get_followers(username):
    try:
        followers = repository.get_followers(username)
        response = Response(json.dumps(followers))
        response.status = 200
        response.headers["Cache-Control"] = "public, max-age=60"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/follow/<follower>/<followed>", methods=["POST"])
def follow(follower, followed):
    try:
        repository.follow(follower, followed)
        return "OK"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/follow/<follower>/<followed>", methods=["DELETE"])
def unfollow(follower, followed):
    try:
        repository.unfollow(follower, followed)
        return "OK"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
