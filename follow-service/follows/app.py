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
            MATCH (:Person {name: $username})-[:FOLLOWS]->(followed:Person)
            RETURN followed {
                username: followed.name
            }
        """
        result = session.run(query, username=username)

        for record in result:
            following.append(record.values()[0]["username"])

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
