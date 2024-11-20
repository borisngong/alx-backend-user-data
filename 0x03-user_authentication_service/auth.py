#!/usr/bin/env python3
"""
Module for working with authentication
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pw
