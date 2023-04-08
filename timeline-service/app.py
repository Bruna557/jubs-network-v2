from datetime import datetime
from flask import Flask, json, request, Response
import logging
import requests
import time

import repository as cache

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/timeline/<username>", methods=["GET"])
def get_timeline(username):
    try:
        logging.info("Fetching posts")
        time = request.args.get("time") or int(datetime.timestamp(datetime.now()))
        scroll = request.args.get("scroll") or "down"

        posts = json.loads(cache.get(username))

        if posts and ((scroll == "down" and get_post_timestamp(posts[-1:][0]) > int(time)) or
                      (scroll == "up" and  get_post_timestamp(posts[0]) < int(time))):
            logging.info("Cache hit - getting posts from cache")
            posts = posts
        else:
            logging.info("Cache miss - getting posts from Post Service")
            followings_result = requests.get(f"http://localhost:5005/follows/followings/{username}")

            if followings_result.status_code == 200:
                posts_result = requests.get(f"http://localhost:5006/posts?page_size=5&time={time}&scroll={scroll}",
                                            data=json.dumps({ "users": json.loads(followings_result.text) }),
                                            headers={"Content-Type":"application/json"})

                if posts_result.status_code == 200 and json.loads(posts_result.text):
                    posts = json.loads(posts_result.text)
                    cache.set(username, posts_result.text)
                else:
                    return posts_result.text, posts_result.status_code
            else:
                return followings_result.text, followings_result.status_code

        response = Response(json.dumps(posts))
        response.headers["Cache-Control"] = "public, max-age=60"
        response.status = 200

    except Exception as e:
        logging.error(f"Failed to fetch posts: {e}")
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500

    response.headers["Content-Type"] = "application/json"
    return response


def get_post_timestamp(post):
    return int(time.mktime(datetime.strptime(post[1], "%a, %d %b %Y %H:%M:%S GMT").timetuple()))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)
