import datetime
import logging

from app import database as db


logging.basicConfig(level=logging.INFO)


def get_by_users(users, page_size, time, scroll):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Fetching posts")
        if scroll == "down":
            query = session.prepare("SELECT * FROM jubs.posts WHERE username IN ? AND time < ? ORDER BY time DESC "
                                    "LIMIT ? ALLOW FILTERING")
        else:
            query = session.prepare("SELECT * FROM jubs.posts WHERE username IN ? AND time > ? ORDER BY time DESC "
                                    "LIMIT ? ALLOW FILTERING")

        # Turn paging off since Cassandra cannot page queries with both ORDER BY and a IN restriction on the
        # partition key
        query.fetch_size = None

        results = session.execute(query, (users, datetime.datetime.fromtimestamp(int(time)), int(page_size)))
        return list(results)

    except Exception as e:
        logging.error(f"Failed to fetch posts: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()


def get_by_username(username, page_size, time, scroll):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Fetching posts")
        if scroll == "down":
            query = "SELECT * FROM jubs.posts WHERE username = %s AND time < %s ORDER BY time DESC LIMIT %s ALLOW " \
                    "FILTERING"
        else:
            query = "SELECT * FROM jubs.posts WHERE username = %s AND time > %s ORDER BY time DESC LIMIT %s ALLOW " \
                    "FILTERING"

        results = session.execute(query, (username, datetime.datetime.fromtimestamp(int(time)), int(page_size)))
        return list(results)

    except Exception as e:
        logging.error(f"Failed to fetch posts: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()


def create(username, body):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Adding post")
        query = session.prepare("""
           INSERT INTO jubs.posts (username, body, likes, time)
           VALUES (?, ?, ?, ?)
           """)
        session.execute(query, [username, body, 0, datetime.datetime.now()])

    except Exception as e:
        logging.error(f"Failed to create post: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()


def edit(username, time, body):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Updating post")
        session.execute("UPDATE jubs.posts SET body = %s WHERE username = %s AND time = %s", (body, username, time))

    except Exception as e:
        logging.error(f"Failed to update post: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()


def like(username, time):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Incrementing likes")
        post = session.execute("SELECT * FROM jubs.posts WHERE username = %s AND time = %s", (username, time))
        likes = post[0].likes + 1
        session.execute("UPDATE jubs.posts SET likes = %s WHERE username = %s AND time = %s", (likes, username, time))

    except Exception as e:
        logging.error(f"Failed to increment likes: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()


def delete(username, time):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Deleting post")
        session.execute("DELETE FROM jubs.posts username = %s AND time = %s", (username, time))

    except Exception as e:
        logging.error(f"Failed to delete post: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()
