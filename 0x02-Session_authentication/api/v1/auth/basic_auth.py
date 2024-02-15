#!/usr/bin/env python3
"""module for BasicAuth class that handles authentication"""
from flask import request
from base64 import b64decode
from typing import List, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class for handling authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part
        of the Authorization header for a Basic Authentication"""
        if isinstance(authorization_header, str):
            if authorization_header.startswith("Basic "):
                return authorization_header.split()[1]
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """returns the decoded value
        of a Base64 string base64_authorization_header"""
        if isinstance(base64_authorization_header, str):
            try:
                header = b64decode(base64_authorization_header).decode("utf-8")
                return header
            except Exception:
                return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """returns the user email and password from the Base64 decoded value"""
        if isinstance(decoded_base64_authorization_header, str):
            if ":" in decoded_base64_authorization_header:
                return tuple(decoded_base64_authorization_header.split(":", 1))
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            try:
                user = User.search({"email": user_email})
                if user and user[0].is_valid_password(user_pwd):
                    return user[0]
            except Exception:
                return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        user = self.user_object_from_credentials(email, password)
        return user
