from flask import Flask, json, request, Response

from . import reposistory


app = Flask(__name__)


@app.route("/posts/<username>", methods=["GET"])
def get_posts(username):
    try:
        posts = reposistory.get_by_username(username)
        response = Response(json.dumps(posts))
        response.status = 200
        response.headers["Cache-Control"] = "public, max-age=60"

    except Exception as e:
        response = Response(json.dumps({ "error": e }))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/posts/<username>", methods=["POST"])
def create_post(username):
    try:
        reposistory.create(username, request.get_json()["body"])
        return "OK"

    except Exception as e:
        response = Response(json.dumps({ "error": e }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/posts/<id>", methods=["PUT"])
def edit_post(id):
    try:
        reposistory.edit(id, request.get_json()["body"])
        return "OK"

    except Exception as e:
        response = Response(json.dumps({ "error": e }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/posts/like/<id>", methods=["PUT"])
def like_post(id):
    try:
        reposistory.like(id)
        return "OK"

    except Exception as e:
        response = Response(json.dumps({ "error": e }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/posts/<id>", methods=["DELETE"])
def delete_post(id):
    try:
        reposistory.delete(id)
        return "OK"

    except Exception as e:
        response = Response(json.dumps({ "error": e }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response
