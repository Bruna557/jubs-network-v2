import datetime
import logging
import uuid

from app import database as db


logging.basicConfig(level=logging.INFO)


def get_by_username(username):
    posts = []

    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Fetching posts")
        posts = session.execute("SELECT * FROM posts WHERE username = %s", (username, ))

    except Exception as e:
        logging.error(f"Failed to fetch posts: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()

    return list(posts)


def create(username, body):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Adding post")
        query = session.prepare("""
           INSERT INTO posts (id, username, body, likes, time)
           VALUES (?, ?, ?, ?, ?)
           """)
        session.execute(query, [uuid.uuid4(), username, body, 0, datetime.datetime.now()])

    except Exception as e:
        logging.error(f"Failed to create post: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()


def edit(id, body):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Updating post")
        session.execute("UPDATE posts SET body = %s WHERE id = %s", (body, uuid.UUID(id)))

    except Exception as e:
        logging.error(f"Failed to update post: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()


def like(id):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Incrementing likes")
        post = session.execute("SELECT * FROM posts WHERE id = %s", (uuid.UUID(id), ))
        likes = post[0].likes + 1
        session.execute("UPDATE posts SET likes = %s WHERE id = %s", (likes, uuid.UUID(id)))

    except Exception as e:
        logging.error(f"Failed to increment likes: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()


def delete(id):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Deleting post")
        session.execute("DELETE FROM posts WHERE id = %s", (uuid.UUID(id), ))

    except Exception as e:
        logging.error(f"Failed to delete post: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()
