#!/usr/bin/env python3
"""
Module for working with Flask app
"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
auth = Auth()

@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    Responsible for handling the get route
    """
    return jsonify({"message" : "Bienvenue"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
