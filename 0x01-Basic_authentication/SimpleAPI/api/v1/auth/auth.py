#!/usr/bin/env python3
"""Module for working with Basic authentication"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Public method that returns False """
        if path is None:
            return True
        
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        
        # normalise_path = path if path.endswith('/') else path + '/'
        if not path.endswith('/'):
            path += '/'
        
        for excluded_p in excluded_paths:
            if not excluded_p.endswith('/'):
                excluded_p += '/'
            if path == excluded_p:
                return False
        return True
    
    def authorization_header(self, request=None) -> str:
        """
        Responsible for returning Authorization header of request object
        """
        if request is None and 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')
    
    def current_user(self, request=None) -> TypeVar('User'):
        """Current user """
        return None