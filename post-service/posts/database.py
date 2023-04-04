
from cassandra.cluster import Cluster
import logging


logging.basicConfig(level=logging.INFO)


def cassandra_connection():
    """
    Connection object for Cassandra
    :return: session, cluster
    """
    cluster = Cluster(["127.0.0.1"], port=9042)
    session = cluster.connect()
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS jubs
        WITH REPLICATION =
        { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
        """)
    session.set_keyspace("jubs")
    return session, cluster


if __name__ == "__main__":
    logging.info("Not callable")