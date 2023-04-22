import logging

from app import database as db
from app.utils import hash_password, get_encoded_jwt


def add(username, password, bio, picture):
    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        logging.info("Adding user")
        hashed_password = hash_password(password)
        query = "MERGE (:Person {username: $username, passowrd: $password, bio: $bio, picture: $picture})"
        session.run(query, username=username, password=hashed_password, bio=bio, picture=picture)

        return get_encoded_jwt(username)
    except Exception as e:
        logging.error(f"Failed to create user: {e}")
        raise e

    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()


def get_by_username(username):
    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        logging.info("Fetching user")
        query = """
            MATCH (user:Person {username: $username})
            RETURN user {
                username: user.username,
                bio: user.bio,
                picture: user.picture
            }
        """
        result = session.run(query, username=username)
        return result.data()

    except Exception as e:
        logging.error(f"Failed to fetch user: {e}")
        raise e

    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()


def search(username, q, page_size, page_number):
    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        logging.info("Searching users")
        query = """
            MATCH (user:Person)
            WHERE user.username STARTS WITH $q
            RETURN user {
                username: user.username,
                bio: user.bio,
                picture: user.picture
                is_followed: EXISTS( (:Person {username: $username})-[:FOLLOWS]->(:Person {username: user.username}) )
            }
            SKIP $skip
            LIMIT $limit
        """
        result = session.run(query, q=q, username=username, skip=int(page_size)*(int(page_number)-1), limit=int(page_size))
        return [record.data() for record in result]

    except Exception as e:
        logging.error(f"Failed to search users: {e}")
        raise e

    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()


def update_password(username, password):
    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        logging.info("Updating password")
        hashed_password = hash_password(password)
        query = """
            MATCH (user:Person {username: $username})
            SET user.password = $password
        """
        result = session.run(query, username=username, password=hashed_password)
        return result

    except Exception as e:
        logging.error(f"Failed to update password: {e}")
        raise e

    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()


def update_bio(username, bio):
    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        logging.info("Updating bio")
        query = """
            MATCH (user:Person {username: $username})
            SET user.bio = $bio
        """
        result = session.run(query, username=username, bio=bio)
        return result

    except Exception as e:
        logging.error(f"Failed to update bio: {e}")
        raise e

    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()


def update_picture(username, picture):
    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        logging.info("Updating picture")
        query = """
            MATCH (user:Person {username: $username})
            SET user.picture = $picture
        """
        result = session.run(query, username=username, picture=picture)
        return result

    except Exception as e:
        logging.error(f"Failed to update picture: {e}")
        raise e

    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()


def get_followings(username, page_size, page_number):
    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        logging.info("Fetching followings")
        query = """
            MATCH (:Person {username: $username})-[:FOLLOWS]->(followed:Person)
            RETURN followed {
                username: followed.username,
                bio: followed.bio,
                picture: followed.picture,
                is_followed: true
            }
        """
        if int(page_size) > -1:
            query += """
                SKIP $skip
                LIMIT $limit
            """
        result = session.run(query, username=username, skip=int(page_size)*(int(page_number)-1), limit=int(page_size))

        return result.data()

    except Exception as e:
        logging.error(f"Failed to fetch followings: {e}")
        raise e

    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()


def get_followers(username, page_size, page_number):
    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        logging.info("Fetching followers")
        query = """
            MATCH (:Person {username: $username})<-[:FOLLOWS]-(follower:Person)
            RETURN follower {
                username: follower.username,
                bio: follower.bio,
                picture: follower.picture,
                is_followed: EXISTS( (:Person {username: $username})-[:FOLLOWS]->(:Person {username: follower.username}) )
            }
        """
        if int(page_size) > -1:
            query += """
                SKIP $skip
                LIMIT $limit
            """
        result = session.run(query, username=username, skip=int(page_size)*(int(page_number)-1), limit=int(page_size))

        return result.data()

    except Exception as e:
        logging.error(f"Failed to fetch followers: {e}")
        raise e

    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()


def get_recommendation(username, page_size, page_number):
    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        logging.info("Fetching followings of followings")
        query = """
            MATCH (user:Person {username: $username})-[:FOLLOWS]->(:Person)-[:FOLLOWS]->(recommendation:Person)
            WHERE user <> recommendation
            AND NOT (:Person {username: $username})-[:FOLLOWS]->(recommendation:Person)
            RETURN recommendation {
                username: recommendation.username
            }
            SKIP $skip
            LIMIT $limit
        """
        result = session.run(query, username=username, skip=int(page_size)*(int(page_number)-1), limit=int(page_size))

        recommendations = [record.values()[0]["username"] for record in result]
        return recommendations

    except Exception as e:
        logging.error(f"Failed to fetch recommendation: {e}")
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
        query = """
            MATCH (u1:Person {username: $user1})
            MATCH (u2:Person {username: $user2})
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
            MATCH (:Person {username: $user1})-[rel:FOLLOWS]->(:Person {username: $user2})
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


def delete(username):
    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        logging.info("Deleting user")
        query = """
            MATCH (m:Person {username: $username})
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


def login(username, password):
    try:
        logging.info("Connecting to Neo4j")
        session, driver = db.neo4j_connection()

        logging.info("Authenticating user")
        hashed_password = hash_password(password)
        query = """
            MATCH (user:Person)
            WHERE user.username = $username AND user.password = $password
            RETURN user
        """
        result = session.run(query, username=username, password=hashed_password)
        if result.data():
            return get_encoded_jwt(username)

    except Exception as e:
        logging.error(f"Failed to authernticate users: {e}")
        raise e

    finally:
        logging.info("Closing connection to Neo4j")
        session.close()
        driver.close()
