
from cassandra.cluster import Cluster
import logging


logging.basicConfig(level=logging.INFO)


def cassandra_connection():
    """
    Connection object for Cassandra
    :return: session, cluster
    """
    cluster = Cluster(["localhost"], port=9042)
    session = cluster.connect()
    return session, cluster


if __name__ == "__main__":
    logging.info("Not callable")
