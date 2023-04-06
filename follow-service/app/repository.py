import logging

from app import database as db


logging.basicConfig(level=logging.INFO)


def get_followings(username):
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

        followings = []
        for record in result:
            followings.append(record.values()[0]["username"])
        return followings

    except Exception as e:
        logging.error(f"Failed to fetch followings: {e}")
        raise e

    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()


def get_followers(username):
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

        followers = []
        for record in result:
            followers.append(record.values()[0]["username"])
        return followers

    except Exception as e:
        logging.error(f"Failed to fetch followers: {e}")
        raise e

    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()


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

    except Exception as e:
        logging.error(f"Failed to add following relationship: {e}")
        raise e

    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()


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

    except Exception as e:
        logging.error(f"Failed to remove following relationship: {e}")
        raise e

    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()


def delete_user(username):
    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        logging.info("Deleting user")
        query = """
            MATCH (m:Person {name: $username})
            DETACH DELETE m
        """
        session.run(query, username=username)

    except Exception as e:
        logging.error(f"Failed to delete user: {e}")
        raise e

    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()
