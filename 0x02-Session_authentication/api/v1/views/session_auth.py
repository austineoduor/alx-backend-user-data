#!/usr/bin/env python3
'''a new Flask view that handles all routes for the Session authentication'''
from flask import (request, Flask, jsonify, abort, session)
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    '''request.form.get() to retrieve email and password parameters
    '''
    if request.method == 'POST':
        mail = request.form.get('email')
        if not mail or mail == '':
            return jsonify({"error": "email missing"}), 400
        pwd = request.form.get('password')
        if not pwd or pwd == '':
            return jsonify({"error": "password missing"}), 400
        ob = User()
        user_ist = ob.search({'email': mail})
        if not user_ist or user_ist == []:
            return jsonify({"error": "no user found for this email"}), 400
        if not user_ist[0].is_valid_password(pwd):
            return jsonify({"error": "wrong password"}), 401

        from api.v1.app import auth
        session_id = auth.create_session(user_ist[0].id)
        re = jsonify(user_ist[0].to_json())
        re.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return re
