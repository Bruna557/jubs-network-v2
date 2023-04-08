from flask import Flask, json, request, Response

from app import reposistory


app = Flask(__name__)


@app.route("/posts", methods=["GET"])
def get_posts():
    try:
        posts = reposistory.get_by_users(request.get_json()["users"],
                                         request.args.get("page_size") or 5,
                                         request.args.get("time"),
                                         request.args.get("scroll") or "down")
        response = Response(json.dumps(posts))
        response.headers["Cache-Control"] = "public, max-age=60"
        response.status = 200

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/posts/<username>", methods=["GET"])
def get_user_posts(username):
    try:
        posts = reposistory.get_by_username(username,
                                            request.args.get("page_size") or 5,
                                            request.args.get("time"),
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
def create_post(username):
    try:
        reposistory.create(username, request.get_json()["body"])
        return "OK"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/posts/<time>/<username>", methods=["PUT"])
def edit_post(time, username):
    try:
        reposistory.edit(username, time, request.get_json()["body"])
        return "OK"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/likes/<time>/<username>", methods=["PUT"])
def like_post(time, username):
    try:
        reposistory.like(username, time)
        return "OK"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/posts/<time>/<username>", methods=["DELETE"])
def delete_post(time, username):
    try:
        reposistory.delete(username, time)
        return "OK"

    except Exception as e:
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
