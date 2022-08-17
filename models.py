import pickle
import sys
from datetime import datetime

from sqlalchemy import Column, Integer, String, BLOB, Float, Boolean, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from config import DB_CONN_STRING

DeclarativeBase = declarative_base()
engine = create_engine(DB_CONN_STRING)
DBSession = sessionmaker(bind=engine)
# db_session = DBSession()


class FileEntry(DeclarativeBase):
    def __init__(self, file_entry_id=None, filename=None, status=None, created=None):
        self.file_entry_id = file_entry_id
        self.filename = filename
        self.status = status
        self.created = created

    # ====== Table options ====== #

    __tablename__ = 'file_entry'

    file_entry_id = Column(Integer(), primary_key=True, nullable=False, autoincrement=True)
    filename = Column(String(255))
    status = Column(String(30))
    created = Column(DateTime(timezone=True), server_default=func.now())


class Word(DeclarativeBase):
    def __init__(self, word_id=None, word=None, filenames=None, count=None):
        self.word_id = word_id
        self.word = word
        self.count = count
        self.filenames = filenames

    # ====== Table options ====== #

    __tablename__ = 'word'

    word_id = Column(Integer(), primary_key=True, nullable=False, autoincrement=True)
    word = Column(String(50))
    count = Column(Integer())
    filenames = Column(BLOB())


DeclarativeBase.metadata.create_all(engine)
DeclarativeBase.metadata.bind = engine
