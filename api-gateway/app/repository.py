import logging


class RedisRepository:
    def __init__(self, db):
        self.db = db

    def get(self, key):
        try:
            logging.info("Connecting to Redis")
            redis_client = self.db.redis_connection()

            result = redis_client.get(key)

        except Exception as e:
            logging.error(f"Error fetching data: {e}")
            raise e

        if result:
            return result.decode("utf-8")
        else:
            return "[]"

    def set(self, key, data):
        try:
            logging.info("Connecting to Redis")
            redis_client = self.db.redis_connection()

            redis_client.set(key, data.encode("utf-8"), redis_client.expiration)

        except Exception as e:
            logging.error(f"Error setting data: {e}")
            raise e
