#!/usr/bin/env python3
"""DB module.
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Responsible for adding  a new user to the database
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user based on a set of filters.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the user.

        Returns:
            User: The first User object found.

        Raises:
            NoResultFound: If no user matches the criteria.
            InvalidRequestError: If the query arguments are invalid.
        """
        fields, values = [], []

        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError(f"Invalid field: {key}")

        # Use the correct filtering method
        result = self._session.query(User).filter(
            tuple_(*fields).in_([tuple(values)])
        ).first()

        if result is None:
            raise NoResultFound("No user found matching the criteria.")

        return result

    def update_user(self, user_id: int, **kwargs) -> User:
        """
        Responsible for updating a user in the database
        """
        try:
            user = self._sesion.query.filter(user_id == user_id).first()
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise InvalidRequestError(f"Invalid field: {key}")
                    self._session.commit()
        except Exception:
            self._session.rollback()
            user = None
        return user
