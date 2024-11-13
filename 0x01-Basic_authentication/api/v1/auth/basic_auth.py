#!/usr/bin/env python3
"""Basic authentication module for the API, providing methods to
handle Basic Authentication by extracting, decoding, and validating
user credentials
"""

import base64
import binascii
import re
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Class that implements Basic Authentication, inheriting from Auth"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header if it follows the
        Basic Authentication scheme ("Basic <token>")

        Args:
            authorization_header (str): The full Authorization header

        Returns:
            str: The Base64-encoded part of the header, or None if the header
            does not contain valid Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        Decodes a Base64-encoded authorization header to retrieve
        the user credentials in plain text.

        Args:
            base64_authorization_header (str): The Base64-encoded credentials

        Returns:
            str: Decoded string in the format "username:password" if success,
            or None if decoding fails
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> Tuple[str, str]:
        """
        Splits the decoded authorization header into user email and password

        Args:
            decoded_base64_authorization_header (str): Decoded header in the
            format "username:password"

        Returns:
            Tuple[str, str]: A tuple containing the username and password
            as strings, or (None, None) if the format is invalid
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        pattern = r'(?P<user>[^:]+):(?P<password>.+)'
        field_match = re.fullmatch(pattern,
                                   decoded_base64_authorization_header.strip())
        if field_match is not None:
            user = field_match.group('user')
            password = field_match.group('password')
            return user, password
        return None, None

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """
        Validates the user's credentials and retrieves the corresponding User
        object if credentials are correct.

        Args:
            user_email (str): User's email.
            user_pwd (str): User's password.

        Returns:
            User: User object if the credentials are valid, otherwise None.
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if len(users) == 0:
            return None
        user = users[0]
        if user.is_valid_password(user_pwd):
            return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the authenticated user based on the request's
        Authorization header

        Args:
            request: HTTP request containing the Authorization header

        Returns:
            User: User object if authentication is successful, otherwise None
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
