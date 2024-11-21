#!/usr/bin/env python3
"""
Module for Flask app for user authentication
"""
from flask import Flask, jsonify, request
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    Handles the root GET route.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    POST /users endpoint to register a user
    Expects:
    - email: The user's email (form data)
    - password: The user's password (form data)
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    POST /sessions route to log in a user.
    Validates user credentials and creates a session.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)

    # Authenticate user
    if not AUTH.valid_login(email, password):
        abort(401)

    # Create session for the user
    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)

    # Set session ID as a cookie in the response
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
