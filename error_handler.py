import os
import sys
import json
import pika

from models import DBSession
from config import (RABBITMQ_CONN_STRING, ERRORS_QUEUE)
from celery_module.tasks import send_email


def main(parsing_channel):
    """
    Reads messages from the errors queue and handles them.
    Sends email with failed filename. Failed sending will retry to send
    up to 99 times with interval of 10 seconds (see celery_module.tasks).
    """

    def callback(ch, method, properties, body):
        """Callback function handles messages from the errors queue"""
        body = json.loads(body.decode('UTF-8'))
        filename = body['filename']
        print(filename)
        send_email.delay(filename)

    parsing_channel.queue_declare(queue=ERRORS_QUEUE)
    parsing_channel.basic_consume(queue=ERRORS_QUEUE,
                                  auto_ack=True,
                                  on_message_callback=callback)
    parsing_channel.start_consuming()


if __name__ == '__main__':
    # Create channel
    parameters = pika.URLParameters(RABBITMQ_CONN_STRING)
    parameters._heartbeat = 0
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    try:
        main(channel)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    finally:
        channel.close()
