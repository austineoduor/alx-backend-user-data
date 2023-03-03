#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
import bcrypt


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''
        has two required string arguments: email and hashed_password
        '''
        if email is not None and (
                hashed_password is not None or hashed_password != ''):
            pwd = bcrypt.hashpw(hashed_password.encode(
                'utf-8'), bcrypt.gensalt())
            ed_user = User(email=email, hashed_password=pwd)
            self._session.add(ed_user)
            self._session.commit()
            return ed_user
