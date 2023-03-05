#!/usr/bin/env python3
'''Hash password'''
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


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


def _generate_uuid() -> str:
    '''
    return a string representation of a new UUID
    '''
    user_uuid = str(uuid.uuid4())
    return user_uuid


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
        """
        checks if the password is correct for the user
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                pwd = user.hashed_password
                prd = password.encode('utf-8')
                return bcrypt.checkpw(prd, pwd)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        '''
        find the user corresponding to the email, generate a new UUID and
        store it in the database as the user’s session_id,
        then return the session ID.
        '''
        try:
            data = self._db.find_user_by(email=email)
            if data:
                session_id = _generate_uuid()
                self._db.update_user(data.id, session_id=session_id)
                return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """ returns the corresponding user """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ The method updates the corresponding user’s session ID to None """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ generates a reset_token for the corresponding user """
        if not email:
            return None
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except Exception as e:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ update the user password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            new_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=new_password,
                                 reset_token=None)
            return None
        except Exception as e:
            raise ValueError
