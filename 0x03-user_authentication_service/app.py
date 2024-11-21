#!/usr/bin/env python3
"""
Module for Flask app for user authentication
"""
from flask import Flask, jsonify, request, redirect, abort
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
        return jsonify({"email": email, "message": "user created"}), 201
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
    return jsonify({"message": "logged out"}), 204


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """GET /profile
    Return:
        - The user's profile information.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    POST /reset_password to generate a password reset token for a user
    """
    email = request.form.get("email")
    if not email:
        abort(400, "Email is required")

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    PUT /reset_password to update the user's password using a reset token
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if not email or not reset_token or not new_password:
        abort(400, "All fields are required")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)