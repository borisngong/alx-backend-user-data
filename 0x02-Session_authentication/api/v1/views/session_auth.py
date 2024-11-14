# api/v1/views/session_auth.py

import os
from typing import Tuple
from flask import jsonify, request, abort
from models.user import User
from api.v1.views import app_views

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """Handles login request with Session ID authentication."""
    email = request.form.get('email')
    if not email or email.strip() == "":
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password or password.strip() == "":
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Import auth only where it's used to avoid circular imports
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    res = jsonify(user.to_json())
    res.set_cookie(os.getenv("SESSION_NAME"), session_id)
    return res

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """Handles logout request by destroying session."""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
