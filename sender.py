import os
import sys
import json
import time
import pika

from models import DBSession, FileEntry
from config import RABBITMQ_CONN_STRING, INPUT_PATH, PARSING_QUEUE, ERRORS_QUEUE


class Sender:
    """Class corresponds sender behaviour"""
    def __init__(self, parsing_channel, errors_channel, db_session):
        self.parsing_channel = parsing_channel
        self.errors_channel = errors_channel
        self.db_session = db_session

    def send(self):
        """
        Handles new files in the INPUT_PATH folder.
        Checks for new files by comparison with database's list of files.
        Creates FileEntry for all new files.
        Sends filename to the corresponding queue depending on file extension:
        'Parsing' queue for *.txt files and to 'Errors' queue for other types
        of files.
        """
        dir_filenames = os.listdir(INPUT_PATH)
        dir_filenames = [INPUT_PATH + filename for filename in dir_filenames]

        db_filenames = self.db_session.query(FileEntry).all()
        db_filenames = [filename.filename for filename in db_filenames]

        for filename in dir_filenames:
            if filename not in db_filenames:
                file_entry = FileEntry(filename=filename, status='new')
                self.db_session.add(file_entry)
                try:
                    self.db_session.commit()
                except Exception:
                    print(sys.exc_info()[1])
                    self.db_session.rollback()

                body = {'filename': filename, 'status': file_entry.status}
                body = json.dumps(body).encode('UTF-8')
                if filename.endswith('.txt'):
                    self.parsing_channel.basic_publish(exchange='',
                                                       routing_key=PARSING_QUEUE,
                                                       body=body)
                else:
                    self.errors_channel.basic_publish(exchange='',
                                                      routing_key=ERRORS_QUEUE,
                                                      body=body)


def get_connections():
    """Returns channels with queues and DB connection"""
    parameters = pika.URLParameters(RABBITMQ_CONN_STRING)
    parameters._heartbeat = 0

    parsing_connection = pika.BlockingConnection(parameters)
    parsing_channel = parsing_connection.channel()
    parsing_channel.queue_declare(queue=PARSING_QUEUE)

    errors_connection = pika.BlockingConnection(parameters)
    errors_channel = errors_connection.channel()
    errors_channel.queue_declare(queue=ERRORS_QUEUE)

    db_session = DBSession()
    return parsing_channel, errors_channel, db_session


def main(parsing_channel, errors_channel, db_session):
    """Main cycle with sender.send() function"""
    sender = Sender(parsing_channel, errors_channel, db_session)
    while True:
        sender.send()
        time.sleep(5)


if __name__ == '__main__':
    # Create input folder if it is not exist
    if not os.path.exists(INPUT_PATH):
        os.makedirs(INPUT_PATH)

    p_channel, e_channel, session = get_connections()
    try:
        main(p_channel, e_channel, session)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    finally:
        p_channel.close()
        e_channel.close()
        session.close()
