#!/usr/bin/env python3
'''a class SessionAuth that inherits from Auth'''
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    '''a class SessionAuth that inherits from Auth
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''creates a Session ID for a user_id
        '''
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''returns a User ID based on a Session ID
        '''
        if session_id is None or not isinstance(session_id, str):
            return None
        if session_id in self.user_id_by_session_id:
            user_id = self.user_id_by_session_id.get(session_id)
            return user_id

    def current_user(self, request=None):
        '''
        (overload) that returns a User instance based on a cookie value
        '''
        cukies = self.session_cookie(request)
        userid = self.user_id_for_session_id(cukies)
        user = User.get(userid)
        return user

    def destroy_session(self, request=None) -> bool:
        '''deletes the user session / logout
        '''
        if request is None:
            return False
        cookie = self.session_cookie(request)
        if not cookie:
            return False
        if not (self.user_id_for_session_id(cookie)):
            return False
        del self.user_id_by_session_id[cookie]
        return True
