import logging
import pandas as pd
import os

from app import database as db


logging.basicConfig(level=logging.INFO)


def add_nodes(df, session):
    for user in df['follower']:
        query = "MERGE (:Person {name: $username})"
        session.run(query, username=user)

    for user in df['followed']:
        query = "MERGE (:Person {name: $username})"
        session.run(query, username=user)


def add_relationships(df, session):
    for follower, followed in zip(df['follower'], df['followed']):
        query = """
            MATCH (u1:Person {name: $user1})
            MATCH (u2:Person {name: $user2})
            CREATE (u1)-[rel:FOLLOWS]->(u2)
        """
        session.run(query, user1=follower, user2=followed)


def main():
    """
    Main script that performs the ETL
    """
    logging.info("Connecting to Neo4j")
    session, driver = db.neo4j_connection()

    try:
        path = os.path.join(os.getcwd() + "/scripts/data/follows.csv")
        df = pd.read_csv(path)

        logging.info("Adding nodes")
        add_nodes(df, session)
        logging.info("Adding relationships")
        add_relationships(df, session)

    except Exception as e:
        print(f"ERROR: {e}")

    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()


if __name__ == "__main__":
    main()
