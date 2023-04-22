import glob
import logging
import os
import pandas as pd
import uuid

from app import database as db


logging.basicConfig(level=logging.INFO)


def transform(df):
    """
    Perform transformation on the data, e.g. droping/addition of columns and conversion of data
    :param df: Pandas Dataframe
    :return: Transformed Pandas Dataframe
    """
    # converting date columns from object to timestamp
    df["posted_on"] =  [pd.Timestamp(t) for t in df["posted_on"]]

    return df


def main():
    """
    Main script that performs the ETL
    """
    logging.info("Connecting to Cassandra")
    session, cluster = db.cassandra_connection()

    try:
        logging.info("Importing data into Pandas Dataframe")
        files = glob.glob(os.path.join(os.getcwd() + "/scripts/data/", "*.csv"))

        separate_dfs = (pd.read_csv(file) for file in files)
        df = pd.concat(separate_dfs, ignore_index=True)

        logging.info("Transforming the data")
        df = transform(df)

        logging.info("Loading data into the table")
        query_insert_posts = "INSERT INTO jubs.posts " \
                                "(posted_by, picture, body, likes, posted_on) " \
                                "VALUES (?, ?, ?, ?, ?)"
        prepared_posts = session.prepare(query_insert_posts)

        for index, row in df.iterrows():
            session.execute(prepared_posts
                            , (row["posted_by"]
                            , row["picture"]
                            , row["body"]
                            , row["likes"]
                            , row["posted_on"]))

    except Exception as e:
        logging.error(f"Error loading data into table: {e}")

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()


if __name__ == "__main__":
    main()
