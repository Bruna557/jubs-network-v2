import logging

from follows import database as db


def main():
    """
    Main script that performs the ETL
    """
    logging.info("Connecting to Neo4j")
    session, driver = db.neo4j_connection()

    try:
        query = """
            LOAD CSV FROM 'file:///./scripts/data/follows.csv' AS row
            MERGE (:Person {name: row[0]})-[:FOLLOWS]->(:Person {name: row[1]})
        """
        session.run(query)

    except Exception as e:
        print(f"ERROR: {e}")

    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()


if __name__ == "__main__":
    main()
