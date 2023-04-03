import glob
import logging
import os
import pandas as pd

from posts import database as db


logging.basicConfig(level=logging.INFO)


def transform(df):
    """
    Perform transformation on the data, e.g. droping/addition of columns and conversion of data
    :param df: Pandas Dataframe
    :return: Transformed Pandas Dataframe
    """
    # converting date columns from object to datetime
    df['time'] =  [pd.Timestamp(t).to_pydatetime() for t in df['time']]
    return df


def main():
    """
    Main script that performs the ETL
    """
    logging.info("Connecting to Cassandra")
    session, cluster = db.cassandra_connection()

    try:
        logging.info("Importing data into Pandas Dataframe that will be used for Cassandra tables")
        files = glob.glob(os.path.join(os.getcwd() + "/scripts/data/", "*.csv"))

        # adding dtype of int for id to prevent Pandas from converting it to a float
        separate_dfs = (pd.read_csv(file, dtype={"id": int}) for file in files)
        df = pd.concat(separate_dfs, ignore_index=True)

        logging.info("Transforming the data")
        df = transform(df)

        logging.info("Loading data into the table")
        query_insert_posts = "INSERT INTO posts " \
                                "(id, username, body, likes, time) " \
                                "VALUES (?, ?, ?, ?, ?)"
        prepared_posts = session.prepare(query_insert_posts)

        for index, row in df.iterrows():
            session.execute(prepared_posts
                            , (row["id"]
                               , row["username"]
                               , row["body"]
                               , row["likes"]
                               , row["time"]))

    except Exception as e:
        print(f"ERROR: {e}")

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()


if __name__ == "__main__":
    main()
