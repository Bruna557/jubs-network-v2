import logging

from app import database as db


logging.basicConfig(level=logging.INFO)


def main():
    """
    Main script that tears down and rebuilds the tables within Cassandra
    """
    session, cluster = db.cassandra_connection()

    try:
        logging.info('Creating keyspace jubs in Cassandra')
        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS jubs
            WITH REPLICATION =
            { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
            """)

        drop_table = "DROP TABLE IF EXISTS posts"
        session.execute(drop_table)

        create_posts_table = "CREATE TABLE IF NOT EXISTS posts "\
                                    "(id uuid" \
                                    ", username text" \
                                    ", body text" \
                                    ", likes int" \
                                    ", time timestamp" \
                                    ", PRIMARY KEY (id))"
        logging.info('Creating posts table in Cassandra')
        session.execute(create_posts_table)
        session.execute("CREATE INDEX username_idx ON posts ( username )")


    except Exception as e:
        print(f"ERROR: {e}")

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()


if __name__ == "__main__":
    main()
