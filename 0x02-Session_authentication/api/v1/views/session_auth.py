#!/usr/bin/env python3
"""Module of session authenticating views.
"""
import os
from typing import Tuple
from flask import abort, jsonify, request

from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """
    Handle user login for session authentication, Log in a user and
    create a session
    Return:
      - JSON representation of a User object
    """
    email = request.form.get('email')
    if not email or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if user.is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        response = jsonify(user.to_json())
        response.set_cookie(os.getenv("SESSION_NAME", "_my_session_id"), session_id)
        return response

    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """log out a user and destroy the session
    Return:
      - An empty JSON object.
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
