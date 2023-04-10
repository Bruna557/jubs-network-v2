from flask import Flask, json, request, Response

from app import reposistory
from app.auth import is_authorized


app = Flask(__name__)


@app.route("/posts", methods=["GET"])
def get_posts():
    try:
        posts = reposistory.get_by_users(request.get_json()["users"],
                                         request.args.get("page_size") or 5,
                                         request.args.get("posted_on"),
                                         request.args.get("scroll") or "down")
        response = Response(json.dumps(posts))
        response.headers["Cache-Control"] = "public, max-age=60"
        response.status = 200

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/posts/<username>", methods=["POST"])
@is_authorized
def create_post(username):
    try:
        reposistory.create(username, request.get_json()["body"])
        return "OK"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/posts/<username>/<posted_on>", methods=["PUT"])
@is_authorized
def edit_post(username, posted_on):
    try:
        reposistory.edit(username, posted_on, request.get_json()["body"])
        return "OK"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/likes/<username>/<posted_on>", methods=["PUT"])
def like_post(username, posted_on):
    try:
        reposistory.like(username, posted_on)
        return "OK"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/posts/<username>/<posted_on>", methods=["DELETE"])
@is_authorized
def delete_post(username, posted_on):
    try:
        reposistory.delete(username, posted_on)
        return "OK"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
