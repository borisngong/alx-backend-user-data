#!/usr/bin/env python3
"""
Module for working with Flask app's user authentication
"""
from flask import Flask, jsonify, request, abort, redirect, make_response
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    Responsible for handling the root route
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
    Responsible for handling user login
    """
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """
    Responsible for handling user logout by destroying the session
    """
    # Retrieve session_id from cookies
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    # Destroy the session
    AUTH.destroy_session(user.id)
    # redirects to homepage
    return redirect("/")


@app.route('/profile', methods=['GET'])
def profile():
    """
    GET /profile endpoint to retrieve the user's profile
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    user_profile = jsonify({"email": user.email}), 200
    return user_profile


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    POST /reset_password endpoint to generate a password reset token
    """
    email = request.form.get("email")
    reset_token = None
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        reset_token = None
    if reset_token is None:
        abort(403)
    reset_tok = jsonify({"email": email, "reset_token": reset_token}), 200
    return reset_tok


@app.route('/reset_password', methods=['PUT'])
def update_password():
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(email, reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    PUT /reset_password
    Responsible for handling password reset requests by validating the
    reset token and updating the user's password
    """
    # Retrieve form data
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    
    # Check if all required fields are provided
    if not email or not reset_token or not new_password:
        abort(400, description="Missing required fields")
    
    try:
        # Attempt to update the password using the provided information
        AUTH.update_password(email, reset_token, new_password)
    except ValueError:
        # Invalid token or email, returning Forbidden status
        abort(403, description="Invalid reset token")
    
    # If everything is successful, return the success response
    return jsonify({"email": email, "message": "Password updated"})



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
