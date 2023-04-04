from flask import Flask, json, Response
import logging

from . import database as db

app = Flask(__name__)


@app.route("/posts/<username>", methods=["GET"])
def get_posts(username):
    posts = []

    try:
        logging.info("Connecting to Cassandra")
        session, cluster = db.cassandra_connection()
        logging.info("Fetching posts")
        posts = session.execute("SELECT * FROM posts WHERE username = %s ALLOW FILTERING", (username, ))

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
