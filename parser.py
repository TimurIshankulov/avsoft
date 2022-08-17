import os
import sys
import json
import re
import pickle
import pika

from models import DBSession, Word
from config import RABBITMQ_CONN_STRING, PARSING_QUEUE


def read_file(filename):
    """Reads file and returns lines of it"""
    try:
        with open(filename, 'r', encoding='UTF-8') as f:
            lines = f.readlines()
    except OSError:
        return []
    return lines


def main(parsing_channel):
    """
    Reads messages from the parsing queue and handles them.
    Extracts words from file and write them to the database.
    If word already exists in the database, it will increase its count
    by one and add filename to the filenames list.
    """
    def callback(ch, method, properties, body):
        """Callback function handles messages from the parsing queue"""
        db_session = DBSession()
        body = json.loads(body.decode('UTF-8'))
        filename = body['filename']

        lines = read_file(filename)
        for line in lines:
            words = re.split(r'[^a-zA-Zа-яА-Я]+', line)
            for word in words:
                if not word:
                    continue
                db_word = db_session.query(Word).filter_by(word=word).first()
                if db_word is None:
                    word_to_add = Word(word=word.lower(), count=1,
                                       filenames=pickle.dumps([filename]))
                    db_session.add(word_to_add)
                else:
                    db_word.count += 1
                    # Load list from db.word.filename (BLOB) via pickle
                    filenames_list = pickle.loads(db_word.filenames)
                    if filename not in filenames_list:
                        filenames_list.append(filename)
                        db_word.filenames = pickle.dumps(filenames_list)
                try:
                    db_session.commit()
                except Exception:
                    print(sys.exc_info()[1])
                    db_session.rollback()

        db_session.close()

    parsing_channel.queue_declare(queue=PARSING_QUEUE)
    parsing_channel.basic_consume(queue=PARSING_QUEUE,
                                  auto_ack=True,
                                  on_message_callback=callback)
    parsing_channel.start_consuming()


if __name__ == '__main__':
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
