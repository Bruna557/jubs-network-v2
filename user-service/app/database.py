from pymongo import MongoClient
import logging


logging.basicConfig(level=logging.INFO)


def mongo_connection():
    """
    Connection object for MongoDB
    :return: database
    """
    client = MongoClient(host="localhost",
                         port=27017,
                         username="jubs",
                         password="12345678",
                         authSource="admin")
    db = client["jubs"]
    return db


if __name__ == "__main__":
    logging.info("Not callable")
