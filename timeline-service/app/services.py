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

    def get(self, username, posted_on, scroll, token):
        try:
            logging.info("Fetching posts")
            posts = json.loads(self.repository.get(username))

            if posts and ((scroll == "down" and _get_post_timestamp(posts[-1:][0]) < int(posted_on)) or
                          (scroll == "up" and _get_post_timestamp(posts[0]) > int(posted_on))):
                logging.info("Cache hit - getting posts from cache")
            else:
                logging.info("Cache miss - getting posts from Post Service")
                followings_result = requests.get(f"http://localhost:5005/follows/followings/{username}",
                                                 headers={"Authorization": f"Bearer {token}"})

                if followings_result.status_code != 200:
                    raise Exception(followings_result.text)

                users = json.loads(followings_result.text)
                users.append(username)

                posts_result = requests.get(f"http://localhost:5006/posts?page_size=5&posted_on={posted_on}&scroll={scroll}",
                                            data=json.dumps({"users": users}),
                                            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

                if posts_result.status_code != 200:
                    raise Exception(posts_result.text)

                posts = json.loads(posts_result.text)
                self.repository.set(username, posts_result.text)

            return posts

        except Exception as e:
            logging.error(f"Failed to fetch posts: {e}")
            raise e
