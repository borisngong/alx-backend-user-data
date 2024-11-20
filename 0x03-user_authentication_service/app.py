#!/usr/bin/env python3
"""
Module for working with Flask app
"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
Auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    Responsible for handling the get route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """
    Endpoint to register a User, which expects email and pw
    in form data
    """
    email = request.get.form('email')
    password = request.get.form('password')
    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400
    try:
        user = AUTH.register(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
