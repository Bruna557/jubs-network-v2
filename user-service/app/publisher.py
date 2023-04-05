import logging
import pika


def publish_user_deleted_event(username):
    logging.info("Publishing UserDeleted event")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='user-deleted', exchange_type='fanout')

    channel.basic_publish(exchange='user-deleted', routing_key='', body=username)
    connection.close()
