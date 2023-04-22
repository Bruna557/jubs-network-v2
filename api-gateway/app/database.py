import logging
import redis


def redis_connection():
    """
    Connection object for Redis
    :return: Redis client
    """
    client = redis.Redis(
        host="localhost",
        port=6379,
        password="psw231377",
        db=0)
    client.expiration = 300
    return client


if __name__ == "__main__":
    logging.info("Not callable")
