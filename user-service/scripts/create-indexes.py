import logging
from pymongo import DESCENDING

from app import database as db


logging.basicConfig(level=logging.INFO)


def main():
    """
    Main script that creates the indexes
    """
    logging.info("Connecting to MongoDB")
    jubs_db = db.mongo_connection()

    try:
        logging.info("Creating username index")
        jubs_db.users.create_index([("name", DESCENDING)])

    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
