#!/usr/bin/env python3
"""module for Auth class that handles authentication"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """Auth class for handling authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns True if the path is not in the list of
        strings excluded_paths"""
        if path and not path.endswith("/"):
            path = path + "/"
        if path is None or not excluded_paths or path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """returns the value of the Authorization request header"""
        if request:
            authorization = request.headers.get("Authorization")
            if authorization:
                return authorization
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None"""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request:
            return request.cookies.get(getenv("SESSION_NAME"))
        return None
