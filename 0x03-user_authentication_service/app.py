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
def login() -> str:
    """
    POST /sessions route to log in a user.
    Validates user credentials and creates a session.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate input
    if not email or not password:
        return jsonify({"message": "email and password are required"}), 401

    # Authenticate user credentials
    if not AUTH.valid_login(email, password):
        return jsonify({"message": "invalid credentials"}), 401

    # Create a session for the user
    session_id = AUTH.create_session(email)
    if session_id is None:
        return jsonify({"message": "session creation failed"}), 401

    # Prepare the response with the session ID as a cookie
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """
    DELETE /sessions route to log out a user.
    Destroys the user session based on the session ID in the cookie.
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        return jsonify({"message": "session_id is required"}), 403

    # Find the user associated with the session ID
    user_email = AUTH.get_user_from_session(session_id)

    if user_email is None:
        return jsonify({"message": "session not found"}), 403

    # Destroy the session
    AUTH.destroy_session(user_email)

    # Redirect to the home page
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """
    GET /profile route to retrieve user profile information.
    Requires a valid session_id cookie.
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        return jsonify({"message": "session_id is required"}), 403

    user_email = AUTH.get_user_from_session(session_id)
    
    if user_email is None:
        return jsonify({"message": "session not found"}), 403
    return jsonify({"email": user_email}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
