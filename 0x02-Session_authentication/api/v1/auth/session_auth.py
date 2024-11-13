#!/usr/bin/env python3
"""
Module for working with Session Authentication
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    Session authentication class inheriting from Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session ID for a user ID
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        # Generate a new session ID
        session_id = str(uuid.uuid4())
        # Store the session ID in the dictionary
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID based on a session ID
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)