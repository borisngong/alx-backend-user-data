#!/usr/bin/env python3
"""
Module for working with authentication
"""

from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import bcrypt
from typing import Union
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
        Responsible for checking if a user's login details are valid
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                is_valid = bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password,
                )
                return is_valid
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

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Responsible for retrieving a user based on a given session ID
        """
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Responsible for destroying a session associated with a given user
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Responsible for generating a password reset token for a user
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Responsible for updating a user's password given the user's reset token
        """
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        new_password_hash = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=new_password_hash,
            reset_token=None,
        )
