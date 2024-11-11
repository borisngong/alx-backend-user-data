#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth  # Import BasicAuth
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize auth
auth = None

# Load the correct instance of Auth based on AUTH_TYPE
auth_type = os.getenv('AUTH_TYPE')
if auth_type == "basic_auth":  # Check for basic_auth
    auth = BasicAuth()  # Use BasicAuth
else:
    auth = Auth()  # Fallback to Auth

# Define the before_request handler
@app.before_request
def before_request():
    """
    Handler for validating request before validating them
    """
    if auth is None:
        return
    # Filter requests before they reach the route handlers
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']
    
    if request.path not in excluded_paths:
        # Check if authentication is required
        if auth.require_auth(request.path, excluded_paths):
            if auth.authorization_header(request) is None:
                abort(401)  # Unauthorized
            if auth.current_user(request) is None:
                abort(403)  # Forbidden

@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """Handler for all unauthorized errors"""
    return jsonify({'error': "unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """Handler for all forbidden errors"""
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)