import logging

import database as db


logging.basicConfig(level=logging.INFO)


def get(key):
    try:
        logging.info("Connecting to Redis")
        redis_client = db.redis_connection()

        result = redis_client.get(key)

    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        raise e

    if result:
        return result.decode("utf-8")
    else:
        return "[]"


def set(key, data):
    try:
        logging.info("Connecting to Redis")
        redis_client = db.redis_connection()

        redis_client.set(key, data.encode("utf-8"), redis_client.expiration)

    except Exception as e:
        logging.error(f"Error setting data: {e}")
        raise e
