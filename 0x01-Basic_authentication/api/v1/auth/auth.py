#!/usr/bin/env python3
"""module for Auth class that handles authentication"""
from typing import List, TypeVar


class Auth:
    """Auth class for handling authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns True if the path is not in the list of
        strings excluded_paths"""
        if path and excluded_paths:
            if not path.endswith("/"):
                path = path + "/"
            for excluded_path in excluded_paths:
                if (excluded_path.endswith("*")
                        and path.startswith(excluded_path[:-1])) or (
                            path == excluded_path
                        ):
                    return False
        return True

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
