#!/usr/bin/env python3
'''Hash password'''
import bcrypt


def _hash_password(password: str) -> str:
    '''
    a _hash_password method that takes in a password
    string arguments and returns bytes.
    '''
    pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return pwd
