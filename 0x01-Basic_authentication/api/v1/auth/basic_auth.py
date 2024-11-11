#!/usr/bin/env python3
"""Module for Basic Authentication that inherits from Auth."""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic Authentication class that extends Auth."""
    
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts the Base64 part of the authorization header.
        
        Args:
            authorization_header (str): The authorization header.

        Returns:
            str: The Base64 encoded string if valid, None otherwise.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        
        # Return the part after 'Basic '
        return authorization_header[6:]