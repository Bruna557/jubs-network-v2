import logging

from app import database as db


logging.basicConfig(level=logging.INFO)


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
