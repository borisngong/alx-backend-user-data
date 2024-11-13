#!/usr/bin/env python3
"""Module for Basic Authentication that inherits from Auth"""
from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """Basic Authentication class that extends Auth"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        # Return the part after 'Basic '
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Decodes the Base64 authorization header"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            # Decode Base64 string
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> str:
        """Extracts user email and password from the decoded Base64 string"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split string at first
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Extracts a user based on the user's authentication credentials.
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance based on the authentication
        """

        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        b64_auth_tok = self.extract_base64_authorization_header(auth_header)
        if b64_auth_tok is None:
            return None

        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        if auth_token is None:
            return None

        email, password = self.extract_user_credentials(auth_token)
        if email is None or password is None:
            return None

        return self.user_object_from_credentials(email, password)

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Extracts the user email and password from the Base64 decoded
        authorization header
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password


def extract_user_credentials(self,
                             decoded_base64_authorization_header: str
                             ) -> Tuple[str, str]:
    """
    Extracts user credentials from a base64-decoded authorization header
    following the Basic authentication scheme
    """
    if isinstance(decoded_base64_authorization_header, str):
        pattern = r'(?P<user>[^:]+):(?P<password>.+)'
        field_match = re.fullmatch(
            pattern,
            decoded_base64_authorization_header.strip(),
        )
        if field_match is not None:
            user = field_match.group('user')
            password = field_match.group('password')
            return user, password

    return None, None
