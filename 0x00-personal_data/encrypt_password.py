#!/usr/bin/env python3
"""Module for working Hass password"""


import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password with bycrypt"""

    salt = bcrypt.gensalt()

    hashed_pw = bcrypt.hashpw(password.encode(), salt)

    return hashed_pw


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Responsible for validating that a password matches a given hashed password
    """
    valid_pw = bcrypt.checkpw(password.encode(), hashed_password)
    return valid_pw
