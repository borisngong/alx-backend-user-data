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


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    POST /sessions route for logging in a user
    """
    # Retrieve email and password from the request form
    email = request.form.get("email")
    password = request.form.get("password")

    # Validate login credentials using the AUTH service
    if not AUTH.valid_login(email, password):
        # If credentials are invalid, respond with HTTP 401 Unauthorized
        abort(401)

    # Create a session ID for the user
    session_id = AUTH.create_session(email)

    # Prepare a JSON response indicating successful login
    response = jsonify({"email": email, "message": "logged in"})

    # Set the session_id as a cookie in the response
    response.set_cookie("session_id", session_id)

    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)