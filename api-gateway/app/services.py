from flask import json
import logging

from app import utils


class TimelineService:
    def __init__(self, repository):
        self.repository = repository

    def get(self, username, posted_on, scroll):
        logging.info("Fetching posts")
        cached = self.repository.get("timeline->" + username)
        cached_json = json.loads(cached)

        if "posts" in cached_json and cached_json["posts"] and \
            ((scroll == "down" and utils.get_post_timestamp(cached_json["posts"][-1:][0]) < int(posted_on)) or
                (scroll == "up" and utils.get_post_timestamp(cached_json["posts"][0]) > int(posted_on))):
            logging.info("Cache hit - getting posts from cache")
            return cached, 200
        else:
            logging.info("Cache miss - getting posts from Post Service")
            res, status_code = utils.get_followings(username, -1, 1)

            if status_code != 200:
                return "Failed to fetch followings", 500

            users = [r["username"] for r in json.loads(res)["result"]]
            users.append(username)

            res, status_code = utils.get_posts(users, posted_on, scroll)

            if status_code != 200:
                return "Failed to fetch posts", 500

            self.repository.set("timeline->" + username, res)

            return res, 200


class AuthService:
    def __init__(self, repository):
        self.repository = repository

    def blacklist(self, username, token):
        self.repository.set("blacklist->" + username, token)

    def verify(self, token, username):
        decoded_token = utils.decode_token(token)
        blacklisted_tokens = self.repository.get("blacklist->" + decoded_token["user"])
        for t in blacklisted_tokens:
            if token == t:
                return False
        if username:
            return decoded_token["user"] == username
        return True
