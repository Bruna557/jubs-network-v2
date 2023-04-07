from datetime import datetime
from flask import Flask, json, request, Response
import logging
import requests

import repository as cache

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/timeline/<username>", methods=["GET"])
def get_timeline(username):
    try:
        logging.info("Fetching posts")
        time = request.args.get("time") or int(datetime.timestamp(datetime.now()))
        scroll = request.args.get("scroll") or "down"

        posts = cache.get(username)

        if posts and ((scroll == "down" and json.loads(posts)[-1:]["time"] > time) or
                      (scroll == "up" and  json.loads(posts)[0]["time"] < time)):
            logging.info("Cache hit - getting posts from cache")
            posts = json.loads(posts)
        else:
            logging.info("Cache miss - getting posts from Post Service")
            followings = requests.get(f"http://localhost:5005/follows/followings/{username}")

            print(f"$$$$$$$$$$$$ Got followings: {followings.text}")

            posts = requests.get(f"http://localhost:5006/posts?page_size=5&time={time}&scroll={scroll}",
                                 data=json.dumps({ "users": list(followings.text) }),
                                 headers={"Content-Type":"application/json"})

            print(f"$$$$$$$$$$$ Got posts: {posts.text}")

            cache.set(username, json.dumps(posts.text))

        response = Response(json.dumps(posts.text))
        response.headers["Cache-Control"] = "public, max-age=60"
        response.status = 200

    except Exception as e:
        logging.error(f"Failed to fetch posts: {e}")
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)
