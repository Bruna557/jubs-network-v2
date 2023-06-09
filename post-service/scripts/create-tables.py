import logging

from app import database as db


logging.basicConfig(level=logging.INFO)


def main():
    """
    Main script that tears down and rebuilds the tables within Cassandra
    """
    session, cluster = db.cassandra_connection()

    logging.info("Creating keyspace jubs in Cassandra")
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS jubs
        WITH REPLICATION =
        { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
        """)

    try:
        drop_table = "DROP TABLE IF EXISTS jubs.posts"
        session.execute(drop_table)

        create_posts_table = "CREATE TABLE IF NOT EXISTS jubs.posts "\
                                    "(posted_by text" \
                                    ", picture text" \
                                    ", body text" \
                                    ", likes int" \
                                    ", posted_on timestamp" \
                                    ", PRIMARY KEY ((posted_by), posted_on))"
        logging.info("Creating posts table in Cassandra")
        session.execute(create_posts_table)

    except Exception as e:
        logging.error(f"Error creating tables: {e}")

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()


if __name__ == "__main__":
    main()
