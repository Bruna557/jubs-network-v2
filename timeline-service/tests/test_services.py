from flask import json
from mock import patch
import pytest

from app.services import TimelineService


class FakeRepository:
    cache = {}

    def get(self, key):
        try:
            return self.cache[key]
        except KeyError:
            return "[]"

    def set(self, key, data):
        self.cache[key] = json.dumps(data)

    def reset(self):
        self.cache = {}


class Response:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = json.dumps(text)


def test_get():
    repository = FakeRepository()
    timeline_service = TimelineService(repository)

    #
    # 1. Cache is empty
    #

    # 1a. Response from /posts is empty
    posts_response = []
    with patch("requests.get", return_value=Response(200, posts_response)) as requests_mock:
        with patch("logging.info") as logging_mock:
            posts = timeline_service.get("jondoe", 1680975829, "down")
            assert posts == posts_response
            assert requests_mock.call_count == 2
            logging_mock.assert_called_with("Cache miss - getting posts from Post Service")

    # 1b. Response from /posts is not empty
    repository.reset()
    posts_response = [["user1", "Sat, 8 Apr 2023 11:43:49 GMT", "some post", 10],
                      ["user2", "Sat, 7 Apr 2023 09:18:01 GMT", "another post", 17]]
    with patch("requests.get", return_value=Response(200, posts_response)) as requests_mock:
        with patch("logging.info") as logging_mock:
            posts = timeline_service.get("jondoe", 1680975829, "down")
            assert posts == posts_response
            assert requests_mock.call_count == 2
            logging_mock.assert_called_with("Cache miss - getting posts from Post Service")

    # 1c. Error response from /posts
    with patch("requests.get", return_value=Response(500, "some error")) as requests_mock:
        with patch("logging.info") as logging_mock:
            with pytest.raises(Exception):
                timeline_service.get("jondoe", 1680975829, "down")
                requests_mock.assert_called_once()
                logging_mock.assert_called_with("Failed to fetch posts: some error")

    #
    # 2. Cache is not empty
    #
    cached_posts = [["user1", "Sat, 8 Apr 2023 11:43:49 GMT", "some post", 10],
                    ["user2", "Sat, 7 Apr 2023 09:18:01 GMT", "another post", 17],
                    ["user1", "Sat, 6 Apr 2023 17:23:58 GMT", "a third post", 2],
                    ["user2", "Sat, 5 Apr 2023 12:01:29 GMT", "a fourth post", 38]]

    # 2a. Scroll down cache hit
    repository.reset()
    repository.set("jondoe", cached_posts)
    with patch("requests.get") as requests_mock:
        with patch("logging.info") as logging_mock:
            posts = timeline_service.get("jondoe", 1680975829, "down") # time: Sat, 8 Apr 2023 11:43:49 GMT
            assert posts == cached_posts
            requests_mock.assert_not_called()
            logging_mock.assert_called_with("Cache hit - getting posts from cache")

    # 2b. Scroll down cache miss
    repository.reset()
    repository.set("jondoe", cached_posts)
    with patch("requests.get", return_value=Response(200, [])) as requests_mock:
        with patch("logging.info") as logging_mock:
            timeline_service.get("jondoe", 1680706889, "down") # time: Sat, 5 Apr 2023 12:01:29 GMT
            assert requests_mock.call_count == 2
            logging_mock.assert_called_with("Cache miss - getting posts from Post Service")

    # # 2c. Scroll up cache hit
    repository.reset()
    repository.set("jondoe", cached_posts)
    with patch("requests.get") as requests_mock:
        with patch("logging.info") as logging_mock:
            posts = timeline_service.get("jondoe", 1680706889, "up") # time: Sat, 5 Apr 2023 12:01:29 GMT
            assert posts == cached_posts
            requests_mock.assert_not_called()
            logging_mock.assert_called_with("Cache hit - getting posts from cache")

    # 2d. Scroll up cache miss
    repository.reset()
    repository.set("jondoe", cached_posts)
    with patch("requests.get", return_value=Response(200, [])) as requests_mock:
        with patch("logging.info") as logging_mock:
            timeline_service.get("jondoe", 1680975829, "up") # time: Sat, 8 Apr 2023 11:43:49 GMT
            assert requests_mock.call_count == 2
            logging_mock.assert_called_with("Cache miss - getting posts from Post Service")
