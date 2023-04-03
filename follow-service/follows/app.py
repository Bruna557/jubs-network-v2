from flask import Flask, json, Response
import logging

from . import database as db

app = Flask(__name__)


@app.route("/following/<username>", methods=["GET"])
def get_posts(username):
    following = []

    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        query = """
            MATCH (:Person {name: $username})-[:FOLLOWS]->(people:Person)
            RETURN people
        """
        following = session.run(query, username=username)

    except Exception as e:
        print(f"ERROR: {e}")


    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()

    response = Response(json.dumps(following))
    response.headers["Cache-Control"] = "public, max-age=60"
    response.headers["Content-Type"] = "application/json"
    response.status = 201
    return response
