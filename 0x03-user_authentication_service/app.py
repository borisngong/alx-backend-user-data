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
    POST /users endpoint to register a user.
    Expects:
    - email: The user's email (form data)
    - password: The user's password (form data)
    
    Response:
    - If successful, returns a JSON payload:
        {"email": "<email>", "message": "user created"}
    - If email already exists:
        {"message": "email already registered"} (400 status code)
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
