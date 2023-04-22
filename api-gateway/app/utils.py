from datetime import datetime
from flask import json
import jwt
import requests
import time

from app.settings import APP_SETTINGS


def get_posts(users, posted_on, scroll):
    result = requests.get(f"http://localhost:5006/posts?page_size=5&posted_on={posted_on}&scroll={scroll}",
                                data=json.dumps({"users": users}),
                                headers={"Content-Type": "application/json"})

    if result.status_code != 200:
        return result.text, result.status_code

    json_result = json.loads(result.text)
    posts = []
    for post in json_result["posts"]:
        posts.append({
            "username": post[0],
            "posted_on": post[1],
            "body": post[2],
            "likes": post[3],
            "picture": post[4]
        })

    return json.dumps({"posts": posts, "has_more": json_result["has_more"]}), result.status_code


def create_user(data):
    result = requests.post(f"http://localhost:5005/users", data=data, headers={"Content-Type": "application/json"})

    return result.text, result.status_code


def get_user(username):
    result = requests.get(f"http://localhost:5005/users/{username}")

    return result.text, result.status_code


def search_users(username, q, page_size, page_number):
    result = requests.get(f"http://localhost:5005/users/{username}/search?q={q}&page_size={page_size}&page_number={page_number}")

    return result.text, result.status_code


def update_user(username, data):
    result = requests.put(f"http://localhost:5005/users/{username}", data=data,
                          headers={"Content-Type": "application/json"})

    return result.text, result.status_code


def get_followings(username, page_size, page_number):
    result = requests.get(f"http://localhost:5005/followings/{username}?page_size={page_size}&page_number={page_number}")

    return result.text, result.status_code


def get_followers(username, page_size, page_number):
    result = requests.get(f"http://localhost:5005/followers/{username}/?page_size={page_size}&page_number={page_number}")

    return result.text, result.status_code


def get_recommendation(username, page_size, page_number):
    result = requests.get(f"http://localhost:5005/followers/recommendation/{username}/?page_size={page_size}&page_number={page_number}")

    return result.text, result.status_code


def follow(username, followed):
    result = requests.post(f"http://localhost:5005/follow/{username}/{followed}")

    return result.text, result.status_code


def unfollow(username, followed):
    result = requests.delete(f"http://localhost:5005/follow/{username}/{followed}")

    return result.text, result.status_code


def delete_user(username):
    result = requests.delete(f"http://localhost:5005/users/{username}")

    return result.text, result.status_code


def create_post(username, data):
    result = requests.post(f"http://localhost:5006/posts/{username}",
                           data=data,
                           headers={"Content-Type": "application/json"})

    return result.text, result.status_code


def edit_post(username, posted_on, data):
    result = requests.put(f"http://localhost:5006/posts/{username}/{posted_on}",
                           data=data,
                           headers={"Content-Type": "application/json"})

    return result.text, result.status_code


def like_post(username, posted_on):
    result = requests.put(f"http://localhost:5006/likes/{username}/{posted_on}")

    return result.text, result.status_code


def delete_post(username, posted_on):
    result = requests.delete(f"http://localhost:5006/posts/{username}/{posted_on}")

    return result.text, result.status_code


def get_post_timestamp(post):
    return int(time.mktime(datetime.strptime(post["posted_on"], "%a, %d %b %Y %H:%M:%S GMT").timetuple()))


def decode_token(token):
    return jwt.decode(token, APP_SETTINGS["SECRET_KEY"], algorithms=["HS256"])
