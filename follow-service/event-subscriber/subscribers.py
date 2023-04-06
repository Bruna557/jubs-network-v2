import logging
import pika

from app import repository


logging.basicConfig(level=logging.INFO)


def subscribe_to_user_deleted_event():
    logging.info("Subscribing to UserDeleted event")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',))
    channel = connection.channel()

    channel.exchange_declare(exchange='user-deleted', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='user-deleted', queue=queue_name)

    def callback(ch, method, properties, body):
        username = body.decode('utf-8')
        logging.info(f"Received UserDeleted event: {username}")
        repository.delete_user(username)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == "__main__":
    subscribe_to_user_deleted_event()
