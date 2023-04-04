import logging
from pymongo import DESCENDING

from users import database as db


def main():
    """
    Main script that drops all collections
    """
    logging.info("Connecting to MongoDB")
    jubs_db = db.mongo_connection()

    try:
        logging.info("Dropping users")
        jubs_db.users.drop()

    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
