#!/usr/bin/env python3
from flask import (Flask, jsonify, request, abort, make_response, redirect)
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def playload():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def registor():
    email = request.form.get('email')
    pwd = request.form.get('password')
    try:
        user = AUTH.register_user(email, pwd)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    '''
    create a new session for the user,
    store it the session ID as a cookie with key "session_id" on the response
    and return a JSON payload
    '''
    email = request.form.get('email')
    pwd = request.form.get('password')
    if not AUTH.valid_login(email, pwd):
        abort(401)
    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)
    result = make_response(jsonify({'email': email, 'message': 'logged in'}))
    result.set_cookie('session_id', session_id)
    return result


@app.route('/profile', methods=['GET'])
def profile():
    """ finds the corresponding user """
    cookie = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(cookie)
    if user is None:
        abort(403)
    else:
        return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """ responds with a reset_token """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        if not reset_token:
            abort(403)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """ updates the user password """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except Exception as e:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
