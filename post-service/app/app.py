from flask import Flask, json, request, Response
from flask_cors import CORS

from app import reposistory


app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route("/posts", methods=["GET"])
def get_posts():
    try:
        posts, has_more = reposistory.get_by_users(request.get_json()["users"],
                                                   request.args.get("page_size"),
                                                   request.args.get("posted_on"),
                                                   request.args.get("scroll"))
        response = Response(json.dumps({"posts": posts, "has_more": has_more}))
        response.headers["Cache-Control"] = "public, max-age=60"
        response.status = 200

    except Exception as e:
        response = Response(json.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/posts/<username>", methods=["POST"])
def create_post(username):
    try:
        data = request.get_json()
        reposistory.create(username, data["picture"], data["body"])
        response = Response("OK")
        response.status_code = 200

    except Exception as e:
        response = Response(json.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/posts/<username>/<posted_on>", methods=["PUT"])
def edit_post(username, posted_on):
    try:
        reposistory.edit(username, posted_on, request.get_json()["body"])
        response = Response("OK")
        response.status_code = 200

    except Exception as e:
        response = Response(json.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/likes/<posted_by>/<posted_on>", methods=["PUT"])
def like_post(posted_by, posted_on):
    try:
        reposistory.like(posted_by, posted_on)
        response = Response("OK")
        response.status_code = 200

    except Exception as e:
        response = Response(json.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/posts/<username>/<posted_on>", methods=["DELETE"])
def delete_post(username, posted_on):
    try:
        reposistory.delete(username, posted_on)
        response = Response("OK")
        response.status_code = 200

    except Exception as e:
        response = Response(json.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True)
