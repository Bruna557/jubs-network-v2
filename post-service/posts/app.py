import datetime
from flask import Flask, json, request, Response
import logging
import uuid

from . import database as db

app = Flask(__name__)


@app.route("/posts/<username>", methods=["GET"])
def get_posts(username):
    posts = []

    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Fetching posts")
        posts = session.execute("SELECT * FROM posts WHERE username = %s", (username, ))

    except Exception as e:
        print(f"ERROR: {e}")


    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()

    response = Response(json.dumps(list(posts)))
    response.headers["Cache-Control"] = "public, max-age=60"
    response.headers["Content-Type"] = "application/json"
    response.status = 201
    return response


@app.route("/posts/<username>", methods=["POST"])
def create_post(username):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Adding post")
        query = session.prepare("""
           INSERT INTO posts (id, username, body, likes, time)
           VALUES (?, ?, ?, ?, ?)
           """)
        session.execute(query, [uuid.uuid4(), username, request.get_json()["body"], 0, datetime.datetime.now()])

    except Exception as e:
        print(f"ERROR: {e}")


    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()

    return "OK"


@app.route("/posts/<id>", methods=["PUT"])
def edit_post(id):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Updating post")
        session.execute("UPDATE posts SET body = %s WHERE id = %s", (request.get_json()["body"], uuid.UUID(id)))

    except Exception as e:
        print(f"ERROR: {e}")


    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()

    return "OK"


@app.route("/posts/like/<id>", methods=["PUT"])
def like_post(id):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Incrementing likes")
        post = session.execute("SELECT * FROM posts WHERE id = %s", (uuid.UUID(id), ))
        likes = post[0].likes + 1
        session.execute("UPDATE posts SET likes = %s WHERE id = %s", (likes, uuid.UUID(id)))

    except Exception as e:
        print(f"ERROR: {e}")


    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()

    return "OK"


@app.route("/posts/<id>", methods=["DELETE"])
def delete_post(id):
    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()

        logging.info("Deleting post")
        session.execute("DELETE FROM posts WHERE id = %s", (uuid.UUID(id), ))

    except Exception as e:
        print(f"ERROR: {e}")


    finally:
        logging.info("Closing connection to Cassandra")
        session.shutdown()
        cluster.shutdown()

    return "OK"
