from datetime import datetime
from flask import abort, Flask, json, request, Response
from flask_cors import CORS
from functools import wraps
import logging

from app import database as redis
from app.repository import RedisRepository
from app.services import TimelineService, AuthService
from app.settings import APP_SETTINGS


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

        if token:
            if decoded_token := auth_service.verify(token):
                if "username" in request.view_args:
                    if request.view_args["username"] == decoded_token["user"]:
                        return function(*args, **kwargs)
                else:
                    return function(*args, **kwargs)
        return abort(401)

    return decorator


@app.route("/timeline/<username>", methods=["GET"])
@is_authorized
def get_timeline(username):
    try:
        posted_on = request.args.get("posted_on") or int(datetime.timestamp(datetime.now()))
        scroll = request.args.get("scroll") or "down"
        authorization_header = request.headers.get("authorization") or ""
        token = authorization_header.replace("Bearer ", "")

        posts, has_more = timeline_service.get(username, posted_on, scroll, token)

        response = Response(json.dumps({"posts": posts, "has_more": has_more}))
        response.headers["Cache-Control"] = "public, max-age=60"
        response.status = 200

    except Exception as e:
        response = Response(json.dumps({"error": str(e)}))
        response.status = 500

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5007, debug=True)
