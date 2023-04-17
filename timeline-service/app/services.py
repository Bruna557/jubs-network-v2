from datetime import datetime
from flask import json
import logging
import requests
import time


def _get_post_timestamp(post):
    return int(time.mktime(datetime.strptime(post["posted_on"], "%a, %d %b %Y %H:%M:%S GMT").timetuple()))


def _get_followings(username, token):
    followings_result = requests.get(f"http://localhost:5005/followings/{username}?page_size=-1&page_number=1",
                                     headers={"Authorization": f"Bearer {token}"})

    if followings_result.status_code != 200:
        raise Exception(followings_result.text)

    return json.loads(followings_result.text)


def _get_picture(username, token):
    user_result = requests.get(f"http://localhost:5008/users/{username}",
                               headers={"Authorization": f"Bearer {token}"})

    if user_result.status_code != 200:
        raise Exception(user_result.text)

    user = json.loads(user_result.text)
    return user["picture"]


def _get_posts(users, posted_on, scroll, token):
    posts_result = requests.get(f"http://localhost:5006/posts?page_size=5&posted_on={posted_on}&scroll={scroll}",
                                data=json.dumps({"users": users}),
                                headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    if posts_result.status_code != 200:
        raise Exception(posts_result.text)

    json_result = json.loads(posts_result.text)
    posts = []
    for post in json_result["posts"]:
        posts.append({
            "username": post[0],
            "posted_on": post[1],
            "body": post[2],
            "likes": post[3],
            "picture": _get_picture(post[0], token)
        })

    return posts, json_result["has_more"]


class TimelineService:
    def __init__(self, repository):
        self.repository = repository

    def get(self, username, posted_on, scroll, token):
        try:
            logging.info("Fetching posts")
            cached = json.loads(self.repository.get(username))

            if "posts" in cached and cached["posts"] and \
                ((scroll == "down" and _get_post_timestamp(cached["posts"][-1:][0]) < int(posted_on)) or
                 (scroll == "up" and _get_post_timestamp(cached["posts"][0]) > int(posted_on))):
                logging.info("Cache hit - getting posts from cache")
                posts = cached["posts"]
                has_more = cached["has_more"]
            else:
                logging.info("Cache miss - getting posts from Post Service")
                users = _get_followings(username, token)
                users.append(username)
                posts, has_more = _get_posts(users, posted_on, scroll, token)
                self.repository.set(username, json.dumps({"posts": posts, "has_more": has_more}))

            return posts, has_more

        except Exception as e:
            logging.error(f"Failed to fetch posts: {e}")
            raise e
