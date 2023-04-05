from flask import Flask, json, Response
import logging

from app import database as db

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/follows/followings/<username>", methods=["GET"])
def get_followings(username):
    following = []

    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        logging.info("Fetching followings")
        query = """
            MATCH (:Person {name: $username})-[:FOLLOWS]->(followed:Person)
            RETURN followed {
                username: followed.name
            }
        """
        result = session.run(query, username=username)

        for record in result:
            following.append(record.values()[0]["username"])

        response = Response(json.dumps(following))
        response.status = 200
        response.headers["Cache-Control"] = "public, max-age=60"

    except Exception as e:
        logging.error(f"Failed to fetch followings: {e}")
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500


    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/follows/followers/<username>", methods=["GET"])
def get_followers(username):
    following = []

    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        logging.info("Fetching followers")
        query = """
            MATCH (:Person {name: $username})<-[:FOLLOWS]-(followed:Person)
            RETURN followed {
                username: followed.name
            }
        """
        result = session.run(query, username=username)

        response = Response(json.dumps(following))
        response.status = 200
        response.headers["Cache-Control"] = "public, max-age=60"

        for record in result:
            following.append(record.values()[0]["username"])

    except Exception as e:
        logging.error(f"Failed to fetch followers: {e}")
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500


    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/follows/<follower>/<followed>", methods=["POST"])
def follow(follower, followed):
    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        logging.info("Adding following relationship")
        query = "MERGE (:Person {name: $username})"
        session.run(query, username=follower)
        session.run(query, username=followed)

        query = """
            MATCH (u1:Person {name: $user1})
            MATCH (u2:Person {name: $user2})
            MERGE (u1)-[rel:FOLLOWS]->(u2)
        """
        session.run(query, user1=follower, user2=followed)

        return "OK"

    except Exception as e:
        logging.error(f"Failed to add following relationship: {e}")
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()



@app.route("/follows/<follower>/<followed>", methods=["DELETE"])
def unfollow(follower, followed):
    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        logging.info("Removing following relationship")
        query = """
            MATCH (:Person {name: $user1})-[rel:FOLLOWS]->(:Person {name: $user2})
            DELETE rel
        """
        session.run(query, user1=follower, user2=followed)

        return "OK"

    except Exception as e:
        logging.error(f"Failed to remove following relationship: {e}")
        response = Response(json.dumps({ "error": str(e) }))
        response.status = 500
        response.headers["Content-Type"] = "application/json"
        return response


    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()
