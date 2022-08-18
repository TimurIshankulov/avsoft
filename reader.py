import os
import sys
import pickle
import time
import uuid

from models import DBSession, Word
from config import N_TIMES, OUTPUT_PATH


class Reader:
    """Class corresponds reader behaviour"""
    def __init__(self, db_session):
        self.db_session = db_session

    def read(self):
        """
        Reads database and finds all records from Word that meets more than N_TIMES.
        For each record found tries to create output file with the word and list of
        files where word contains. If there is error with removing record from the
        database then output file will be deleted.
        """
        # Commit need for query to be updated, otherwise it will return the same results
        try:
            self.db_session.commit()
        except Exception:
            print(sys.exc_info()[1])
            self.db_session.rollback()

        words = self.db_session.query(Word).filter(Word.count >= N_TIMES)
        for word in words:
            filename = word.word + '__' + str(uuid.uuid4())
            try:
                with open(f'{OUTPUT_PATH}{filename}.txt', 'w', encoding='UTF-8') as f:
                    f.write(word.word + '\n')
                    f.write(' '.join(pickle.loads(word.filenames)))
            except OSError:
                continue
            else:
                self.db_session.delete(word)
                try:
                    self.db_session.commit()
                except Exception:
                    print(sys.exc_info()[1])
                    self.db_session.rollback()
                    # Remove output file if we cannot delete record from DB
                    os.remove(f'{OUTPUT_PATH}{filename}.txt')


def main(db_session):
    """Main cycle with reader.read() function"""
    reader = Reader(db_session)
    while True:
        reader.read()
        time.sleep(10)


if __name__ == '__main__':
    # Create output folder if it is not exist
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    session = None
    for i in range(5):
        try:
            session = DBSession()
        except Exception:
            time.sleep(10)
        else:
            break

    if session is not None:
        try:
            main(session)
        except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        finally:
            session.close()
