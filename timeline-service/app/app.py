from datetime import datetime
from flask import Flask, json, request, Response
import logging

from app import database as redis
from app.repository import RedisRepository
from app.services import TimelineService

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

repository = RedisRepository(redis)
timeline_service = TimelineService(repository)


@app.route("/timeline/<username>", methods=["GET"])
def get_timeline(username):
    try:
        time = request.args.get("time") or int(datetime.timestamp(datetime.now()))
        scroll = request.args.get("scroll") or "down"

        posts = timeline_service.get(username, time, scroll)

        response = Response(json.dumps(posts))
        response.headers["Cache-Control"] = "public, max-age=60"
        response.status = 200

    except Exception as e:
        response = Response(json.dumps({"error": str(e)}))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)
