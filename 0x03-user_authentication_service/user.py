#!/usr/bin/env python3
'''a SQLAlchemy model named User'''
from sqlalchemy import (create_engine, Integer, String, Column)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = create_engine('sqlite:///:memmory:', echo=True)

class User(Base):
    '''
    User for a database table named users
    '''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    '''def __repr__(self):
        sring formatter'''
