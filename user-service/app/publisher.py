import logging
import pika
import time


def connect_to_rabbitmq():
    try:
        return pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    except:
        # RabbitMQ is not up yet
        time.sleep(30)
        return connect_to_rabbitmq()


def publish_user_deleted_event(username):
    logging.info("Publishing UserDeleted event")
    connection = connect_to_rabbitmq()
    channel = connection.channel()

    channel.exchange_declare(exchange="user-deleted", exchange_type="fanout")

    channel.basic_publish(exchange="user-deleted", routing_key="", body=username)
    connection.close()
