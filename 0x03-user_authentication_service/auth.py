#!/usr/bin/env python3
'''Hash password'''
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    '''
    a _hash_password method that takes in a password
    string arguments and returns bytes.
    '''
    if not isinstance(password, bytes):
        prd = password.encode('utf-8')
    else:
        prd = password
    pwd = bcrypt.hashpw(prd, bcrypt.gensalt())
    return pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        '''constructor'''
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''
         take mandatory email and password string arguments and
         return a User object.
        '''
        try:
            if email is not None and password is not None:
                data = self._db.find_user_by(email=email)
                if data:
                    raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            pwd = _hash_password(password)
            user = self._db.add_user(email, pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        '''
        It should expect email and password required arguments
        and return a boolean.
        if email is not None and password is not None
        '''
        try:
            data = self._db.find_user_by(email=email)
            if data:
                if bcrypt.checkpw(password.encode(), data.hashed_password):
                    return True
        except NoResultFound:
            return False
