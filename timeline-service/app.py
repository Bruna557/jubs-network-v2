from flask import Flask, json, Response
import logging
import requests

import database as db

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/timeline/<username>", methods=["GET"])
def get_timeline(username):
    posts = []

    try:
        logging.info("Connecting to Redis")
        cache = db.redis_connection()

        logging.info("Fetching posts")
        posts = cache.get_data(username) or []

        if not posts:
            logging.info("Cache miss - getting posts from Post Service")
            followings = requests.get(f"http://localhost:5005/follows/followings/{username}")
            for user in json.loads(followings.text):
                _posts = requests.get(f"http://localhost:5006/posts/{user}")
                posts.append(json.loads(_posts.text))
            cache.set_data(username, json.dumps(posts))
        else:
            logging.info("Cache hit - getting posts from cache")
            posts = json.loads(posts)

    except Exception as e:
        print(f"ERROR: {e}")

    response = Response(json.dumps(posts))
    response.headers["Cache-Control"] = "public, max-age=60"
    response.headers["Content-Type"] = "application/json"
    response.status = 200
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)
