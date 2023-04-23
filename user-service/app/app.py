from flask import Flask, json, request, Response
from flask_cors import CORS
import logging

from app import repository
from app import publisher


app = Flask(__name__)
CORS(app, supports_credentials=True)
logging.basicConfig(level=logging.INFO)


@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        encoded_jwt = repository.add(data["username"], data["password"], data["bio"], data["picture"])

        response = Response(json.dumps({"token": encoded_jwt}))
        response.status = 200

    except Exception as e:
        response = Response(json.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/users/<username>", methods=["GET"])
def get_user(username):
    try:
        user = repository.get_by_username(username)
        response = Response(json.dumps(user))
        response.headers["Cache-Control"] = "public, max-age=60"
        response.status = 200

    except Exception as e:
        response = Response(json.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/users/<username>/search", methods=["GET"])
def search_users(username):
    try:
        users, has_more = repository.search(username, request.args.get("q"), request.args.get("page_size"),
                                            request.args.get("page_number"))
        response = Response(json.dumps({"result": users, "has_more": has_more}))
        response.headers["Cache-Control"] = "public, max-age=60"
        response.status = 200

    except Exception as e:
        response = Response(json.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/users/<username>", methods=["PUT"])
def edit_user(username):
    try:
        data = request.get_json()

        if "password" in data:
            repository.update_password(username, data["password"])
            data["password"] = "REDACTED"
        if "bio" in data:
            repository.update_bio(username, data["bio"])
        if "picture" in data:
            repository.update_picture(username, data["picture"])

        response = Response(json.dumps(data))
        response.status = 200

    except Exception as e:
        response = Response(json.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/followings/<username>", methods=["GET"])
def get_followings(username):
    try:
        followings, has_more = repository.get_followings(username, request.args.get("page_size"),
                                                         request.args.get("page_number"))
        response = Response(json.dumps({"result": followings, "has_more": has_more}))
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
        followers, has_more = repository.get_followers(username, request.args.get("page_size"),
                                                       request.args.get("page_number"))
        response = Response(json.dumps({"result": followers, "has_more": has_more}))
        response.status = 200
        response.headers["Cache-Control"] = "public, max-age=60"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/followers/recommendation/<username>", methods=["GET"])
def get_recommendation(username):
    try:
        recommendation, has_more = repository.get_recommendation(username, request.args.get("page_size"),
                                                                 request.args.get("page_number"))
        response = Response(json.dumps({"result": recommendation, "has_more": has_more}))
        response.status = 200
        response.headers["Cache-Control"] = "public, max-age=60"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/follow/<username>/<followed>", methods=["POST"])
def follow(username, followed):
    try:
        repository.follow(username, followed)
        response = Response("OK")
        response.status_code = 200

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/follow/<username>/<followed>", methods=["DELETE"])
def unfollow(username, followed):
    try:
        repository.unfollow(username, followed)
        response = Response("OK")
        response.status_code = 200

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/users/<username>", methods=["DELETE"])
def delete_user(username):
    try:
        repository.delete(username)
        publisher.publish_user_deleted_event(username)
        response = Response("OK")
        response.status_code = 200

    except Exception as e:
        response = Response(json.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        token = repository.login(data["username"], data["password"])

        if not token:
            response = Response(json.dumps({"error": "Invalid credentials"}))
            response.status = 401
        else:
            response = Response(json.dumps({"token": token}))
            response.status = 200

    except Exception as e:
        response = Response(json.dumps({"error": str(e)}))
        response.status = 500

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
