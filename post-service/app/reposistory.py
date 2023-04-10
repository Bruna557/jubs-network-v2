import datetime
import logging

from app import database as db

logging.basicConfig(level=logging.INFO)


def get_by_users(users, page_size, posted_on, scroll):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Fetching posts")
        if scroll == "down":
            query = session.prepare("SELECT * FROM jubs.posts WHERE username IN ? AND posted_on < ? ORDER BY posted_on"
                                    " DESC LIMIT ?")
        else:
            query = session.prepare("SELECT * FROM jubs.posts WHERE username IN ? AND posted_on > ? ORDER BY posted_on"
                                    " DESC LIMIT ?")

        # Turn paging off since Cassandra cannot page queries with both ORDER BY and a IN restriction on the
        # partition key
        query.fetch_size = None

        results = session.execute(query, (users, datetime.datetime.fromtimestamp(int(posted_on)), int(page_size)))
        return list(results)

    except Exception as e:
        logging.error(f"Failed to fetch posts: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()


def get_by_username(username, page_size, posted_on, scroll):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Fetching posts")
        if scroll == "down":
            query = "SELECT * FROM jubs.posts WHERE username = %s AND posted_on < %s ORDER BY posted_on DESC LIMIT %s"
        else:
            query = "SELECT * FROM jubs.posts WHERE username = %s AND posted_on > %s ORDER BY posted_on DESC LIMIT %s"

        results = session.execute(query, (username, datetime.datetime.fromtimestamp(int(posted_on)), int(page_size)))
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
           INSERT INTO jubs.posts (username, body, likes, posted_on)
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


def edit(username, posted_on, body):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Updating post")
        session.execute("UPDATE jubs.posts SET body = %s WHERE username = %s AND posted_on = %s",
                        (body, username, posted_on))

    except Exception as e:
        logging.error(f"Failed to update post: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()


def like(username, posted_on):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Incrementing likes")
        post = session.execute("SELECT * FROM jubs.posts WHERE username = %s AND posted_on = %s", (username, posted_on))
        likes = post[0].likes + 1
        session.execute("UPDATE jubs.posts SET likes = %s WHERE username = %s AND posted_on = %s",
                        (likes, username, posted_on))

    except Exception as e:
        logging.error(f"Failed to increment likes: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()


def delete(username, posted_on):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Deleting post")
        session.execute("DELETE FROM jubs.posts username = %s AND posted_on = %s", (username, posted_on))

    except Exception as e:
        logging.error(f"Failed to delete post: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()
