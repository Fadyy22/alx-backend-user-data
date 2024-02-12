#!/usr/bin/env python3
"""module for BasicAuth class that handles authentication"""
from flask import request
from base64 import b64decode
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class for handling authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part
        of the Authorization header for a Basic Authentication"""
        if (not authorization_header
                or not isinstance(authorization_header, str)
                or not authorization_header.startswith("Basic ")):
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """returns the decoded value
        of a Base64 string base64_authorization_header"""
        if (not base64_authorization_header
                or not isinstance(base64_authorization_header, str)):
            return None

        try:
            header = b64decode(base64_authorization_header).decode("utf-8")
        except Exception:
            return None
        return header

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """returns the user email and password from the Base64 decoded value"""
        if (not decoded_base64_authorization_header
                or not isinstance(decoded_base64_authorization_header, str)
                or ":" not in decoded_base64_authorization_header):
            return None
        return tuple(decoded_base64_authorization_header.split(":"))
