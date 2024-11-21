#!/usr/bin/env python3
"""
Module for working with authentication
"""

from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import bcrypt
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    Responsible for generating a unique identifier
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializes a new Auth instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Responsible for registering a new user
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Checks if a user's login details are valid.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password,
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
        Responsible for craeting a new session
        """
        sp_user = None
        try:
            sp_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if sp_user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(sp_user.id, session_id=session_id)
        return session_id
