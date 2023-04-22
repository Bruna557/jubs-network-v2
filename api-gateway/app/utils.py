from datetime import datetime
from flask import json
import jwt
import requests
import time

from app.settings import APP_SETTINGS


def get_post_timestamp(post):
    return int(time.mktime(datetime.strptime(post["posted_on"], "%a, %d %b %Y %H:%M:%S GMT").timetuple()))


def get_followings(username, token):
    followings_result = requests.get(f"http://localhost:5005/followings/{username}?page_size=-1&page_number=1",
                                     headers={"Authorization": f"Bearer {token}"})

    if followings_result.status_code != 200:
        raise Exception(followings_result.text)

    return json.loads(followings_result.text)


def get_posts(username, users, posted_on, scroll, token):
    usernames = [user["username"] for user in users]
    usernames.append(username)
    posts_result = requests.get(f"http://localhost:5006/posts?page_size=5&posted_on={posted_on}&scroll={scroll}",
                                data=json.dumps({"users": usernames}),
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
            "picture": [user.picture for user in users if user.username == post[0]][0]
        })

    return posts, json_result["has_more"]


def decode_token(token):
    return jwt.decode(token, APP_SETTINGS["SECRET_KEY"], algorithms=["HS256"])
