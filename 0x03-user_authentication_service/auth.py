#!/usr/bin/env python3
"""
Module for working with authentication
"""

from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import bcrypt


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

import bcrypt

def _hash_password(password: str) -> bytes:
    """
    Responsible for Hashing a password using bcrypt
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

    def register_user(self, email: str, password: str) -> User:
        """
        Responsible for registering a user
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User  {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            new_user = User(email=email, hashed_password=hashed_password)
            self._db.add_user(new_user)
            return new_user