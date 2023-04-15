from datetime import datetime
from flask import Flask, json, request, Response
import logging

from app import database as redis
from app.auth import is_authorized
from app.repository import RedisRepository
from app.services import TimelineService


app = Flask(__name__)
repository = RedisRepository(redis)
timeline_service = TimelineService(repository)
logging.basicConfig(level=logging.INFO)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5007, debug=True)
