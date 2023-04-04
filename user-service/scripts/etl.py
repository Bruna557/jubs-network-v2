import csv
import logging

from users import database as db


def main():
    """
    Main script that performs the ETL
    """
    logging.info("Connecting to MongoDB")
    jubs_db = db.mongo_connection()

    try:
        logging.info("Importing data")
        header = ["username", "password", "bio", "picture"]
        csvFile = open("scripts/data/users.csv", "r")
        reader = csv.DictReader(csvFile)

        logging.info("Loading data into the collection")
        for each in reader:
            row = {}
            for field in header:
                row[field] = each[field]
            jubs_db["users"].insert_one(row)

    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
