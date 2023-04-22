from flask import json
import logging

from app.utils import get_post_timestamp, get_followings, get_posts, decode_token


class TimelineService:
    def __init__(self, repository):
        self.repository = repository

    def get(self, username, posted_on, scroll, token):
        try:
            logging.info("Fetching posts")
            cached = json.loads(self.repository.get("timeline->" + username))

            if "posts" in cached and cached["posts"] and \
                ((scroll == "down" and get_post_timestamp(cached["posts"][-1:][0]) < int(posted_on)) or
                 (scroll == "up" and get_post_timestamp(cached["posts"][0]) > int(posted_on))):
                logging.info("Cache hit - getting posts from cache")
                posts = cached["posts"]
                has_more = cached["has_more"]
            else:
                logging.info("Cache miss - getting posts from Post Service")
                users = get_followings(username, token)
                posts, has_more = get_posts("timeline->" + username, users, posted_on, scroll, token)
                self.repository.set(username, json.dumps({"posts": posts, "has_more": has_more}))

            return posts, has_more

        except Exception as e:
            logging.error(f"Failed to fetch posts: {e}")
            raise e


class AuthService:
    def __init__(self, repository):
        self.repository = repository

    def blacklist(self, username, token):
        self.repository.set("blacklist->" + username, token)

    def verify(self, token):
        decoded_token = decode_token(token)
        blacklisted_tokens = self.repository.get("blacklist->" + decoded_token["user"])
        for t in blacklisted_tokens:
            if token == t:
                return False
        return decoded_token
