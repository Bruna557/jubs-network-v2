import logging
from neo4j import GraphDatabase


logging.basicConfig(level=logging.INFO)


def neo4j_connection():
    """
    Connection object for Neo4j
    :return: session, driver
    """
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "12345678"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    session = driver.session()

    return session, driver


if __name__ == "__main__":
    logging.info("Not callable")
