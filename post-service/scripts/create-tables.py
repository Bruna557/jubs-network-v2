import logging

from posts import database as db


logging.basicConfig(level=logging.INFO)


def main():
    """
    Main script that tears down and rebuilds the tables within Cassandra
    """
    session, cluster = db.cassandra_connection()

    try:
        drop_table = 'DROP TABLE IF EXISTS posts'
        session.execute(drop_table)

        create_posts_table = "CREATE TABLE IF NOT EXISTS posts "\
                                    "(id int" \
                                    ", username text" \
                                    ", body text" \
                                    ", likes int" \
                                    ", time timestamp" \
                                    ", PRIMARY KEY (id))"
        logging.info('Creating posts table in Cassandra')
        session.execute(create_posts_table)

    except Exception as e:
        print(f'ERROR: {e}')

    finally:
        logging.info('Closing connection to Cassandra')
        session.shutdown()
        cluster.shutdown()


if __name__ == "__main__":
    main()
