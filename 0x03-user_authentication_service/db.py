#!/usr/bin/env python3
"""
Module for working with DB
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
from user import Base, User


class DB:
    """
    DB class for managing database operations.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Save the user to the database

        Args:
            email (str): The user's email
            hashed_password (str): The user's hashed password

        Returns:
            User: The created User object

        Raises:
            SQLAlchemyError: If there is an error during
            the database operation
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
            return user
        except SQLAlchemyError as error:
            self._session.rollback()
            raise error
