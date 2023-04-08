from datetime import datetime
from flask import json
import logging
import requests
import time


def _get_post_timestamp(post):
    return int(time.mktime(datetime.strptime(post[1], "%a, %d %b %Y %H:%M:%S GMT").timetuple()))


class TimelineService:
    def __init__(self, repository):
        self.repository = repository

    def get(self, username, _time, scroll):
        try:
            logging.info("Fetching posts")
            posts = json.loads(self.repository.get(username))

            if posts and ((scroll == "down" and _get_post_timestamp(posts[-1:][0]) < int(_time)) or
                          (scroll == "up" and _get_post_timestamp(posts[0]) > int(_time))):
                logging.info("Cache hit - getting posts from cache")
            else:
                logging.info("Cache miss - getting posts from Post Service")
                followings_result = requests.get(f"http://localhost:5005/follows/followings/{username}")

                if followings_result.status_code != 200:
                    raise Exception(followings_result.text)

                posts_result = requests.get(f"http://localhost:5006/posts?page_size=5&time={_time}&scroll={scroll}",
                                            data=json.dumps({"users": json.loads(followings_result.text)}),
                                            headers={"Content-Type": "application/json"})

                if posts_result.status_code != 200:
                    raise Exception(posts_result.text)

                posts = json.loads(posts_result.text)
                self.repository.set(username, posts_result.text)

            return posts

        except Exception as e:
            logging.error(f"Failed to fetch posts: {e}")
            raise e
