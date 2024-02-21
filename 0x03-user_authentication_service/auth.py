#!/usr/bin/env python3
"""auth module"""
import bcrypt
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers and saves the user to the database"""
        try:
            user = self._db.find_user_by(email=email)
        except InvalidRequestError or NoResultFound:
            hashed_pw = _hash_password(password).decode("utf-8")
            new_user = self._db.add_user(email, password)
            return new_user
        raise ValueError(f"User {email} already exists")


def _hash_password(password: str) -> bytes:
    """method that takes in a password string arguments and returns bytes
    The returned bytes is a salted hash of the input password,
    hashed with bcrypt.hashpw"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
