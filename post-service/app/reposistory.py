from datetime import datetime
import logging

from app import database as db

logging.basicConfig(level=logging.INFO)


def get_by_users(users, page_size, posted_on, scroll):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Fetching posts")
        if scroll == "down":
            query = session.prepare("SELECT * FROM jubs.posts WHERE posted_by IN ? AND posted_on < ? ORDER BY posted_on"
                                    " DESC LIMIT ?")
        else:
            query = session.prepare("SELECT * FROM jubs.posts WHERE posted_by IN ? AND posted_on > ? ORDER BY posted_on"
                                    " DESC LIMIT ?")

        # Turn paging off since Cassandra cannot page queries with both ORDER BY and a IN restriction on the
        # partition key
        query.fetch_size = None

        results = session.execute(query,(users, int(posted_on), int(page_size) + 1))

        posts = list(results)
        if len(posts) > int(page_size):
            has_more = True
            posts = posts[:int(page_size)]
        else:
            has_more = False

        return posts, has_more

    except Exception as e:
        logging.error(f"Failed to fetch posts: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()


def get_by_username(username):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        results = session.execute("SELECT * FROM jubs.posts WHERE posted_by = %s", (username, ))
        return list(results)

    except Exception as e:
        logging.error(f"Failed to fetch posts: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()


def create(username, picture, body):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Adding post")
        query = session.prepare("""
           INSERT INTO jubs.posts (posted_by, picture, body, likes, posted_on)
           VALUES (?, ?, ?, ?, ?)
           """)
        posted_on = datetime.now().replace(microsecond=0)
        likes = 0
        session.execute(query, [username, picture, body, likes, posted_on])
        return {"username": username, "picture": picture, "body": body, "likes": likes, "posted_on": posted_on}

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
        session.execute("UPDATE jubs.posts SET body = %s WHERE posted_by = %s AND posted_on = %s",
                        (body, username, int(posted_on)))

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
        post = session.execute("SELECT * FROM jubs.posts WHERE posted_by = %s AND posted_on = %s",
                               (username, int(posted_on)))
        likes = post[0][3] + 1
        session.execute("UPDATE jubs.posts SET likes = %s WHERE posted_by = %s AND posted_on = %s",
                        (likes, username, int(posted_on)))

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
        session.execute("DELETE FROM jubs.posts WHERE posted_by = %s AND posted_on = %s",
                        (username, int(posted_on) if type(posted_on) == str else posted_on))

    except Exception as e:
        logging.error(f"Failed to delete post: {e}")
        raise e

    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()
