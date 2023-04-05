import logging
import redis


logging.basicConfig(level=logging.INFO)


class RedisDb:
    def __init__(self, host, port, pwd, expiration):
        try:
            self._redis_client = redis.Redis(
                host=host,
                port=port,
                password=pwd,
                db=0)
            self.expiration = expiration
        except Exception as ex:
            logging.error(ex)
            raise ex

    def get_data(self, key):
        try:
            redis_data = self._redis_client.get(key)
        except Exception as ex:
            logging.error(ex)
            raise ex
        else:
            if redis_data is not None:
                return redis_data.decode('utf-8')
            else:
                return None

    def set_data(self, key, data):
        try:
            self._redis_client.set(key, data.encode('utf-8'), self.expiration)
        except Exception as ex:
            logging.error(ex)
            raise ex
        else:
            pass


def redis_connection():
    """
    Connection object for Redis
    :return: database
    """
    db = RedisDb(host='localhost',
                    port=6379,
                    pwd='psw231377',
                    expiration=300)
    return db


if __name__ == "__main__":
    logging.info("Not callable")
