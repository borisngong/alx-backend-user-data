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
    
    def destroy_session(self, request=None):
        """Deletes the user session / logout"""
        if request is None:
            return False

        # Retrieve session ID from request cookies
        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Retrieve user ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        # Delete the session ID from user_id_by_session_id dictionary
        del self.user_id_by_session_id[session_id]
        return True
