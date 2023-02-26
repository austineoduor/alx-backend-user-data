#!/usr/bin/env python3
'''
a new authentication system, based on Session ID stored in database
(for us, it will be in a file, like User)
'''
from models.base import Base


class UserSession(Base):
    '''
    a new model UserSession in models/user_session.py that inherits from Base:
    '''
    def __init__(self, *args: list, **kwargs: dict):
        '''constructor'''
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
