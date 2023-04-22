import logging
import pandas as pd
import os

from app import database as db


logging.basicConfig(level=logging.INFO)


def add_nodes(df, session):
    for index, row in df.iterrows():
        query = "CREATE (:Person {username: $username, password: $password, bio: $bio, picture: $picture})"
        session.run(query, username=row["username"], password=row["password"], bio=row["bio"], picture=row["picture"])


def add_relationships(df, session):
    for follower, followed in zip(df["follower"], df["followed"]):
        query = """
            MATCH (u1:Person {username: $user1})
            MATCH (u2:Person {username: $user2})
            CREATE (u1)-[rel:FOLLOWS]->(u2)
        """
        session.run(query, user1=follower, user2=followed)


def main():
    """
    Main script that performs the ETL
    """
    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        logging.info("Adding nodes")
        path = os.path.join(os.getcwd() + "/scripts/data/users.csv")
        df = pd.read_csv(path)
        add_nodes(df, session)


        logging.info("Adding relationships")
        path = os.path.join(os.getcwd() + "/scripts/data/follows.csv")
        df = pd.read_csv(path)
        add_relationships(df, session)

    except Exception as e:
        logging.error(f"Error adding nodes/relationships: {e}")

    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()


if __name__ == "__main__":
    main()
