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

    def _hash_password(self, password: str) -> bytes:
        """
        Hashes a password using bcrypt.

        Args:
            password (str): The password to hash.

        Returns:
            bytes: The salted hash of the password.
        """
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_pw

    def register_user(self, email: str, password: str) -> User:
        """
        Responsible for registering a user.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            # Check if the user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User  {email} already exists")
        except NoResultFound:
            # User does not exist, proceed to create a new one
            hashed_password = self._hash_password(password)
            new_user = User(email=email, hashed_password=hashed_password)
            self._db.add_user(new_user)
            return new_user