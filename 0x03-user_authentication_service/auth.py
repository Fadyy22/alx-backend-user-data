#!/usr/bin/env python3
"""auth module"""
import bcrypt
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
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
            new_user = self._db.add_user(email, hashed_pw)
            return new_user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """checks if the user entered valid credentials"""
        try:
            user = self._db.find_user_by(email=email)
            encoded_password = password.encode("utf-8")
            encoded_hashed_password = user.hashed_password.encode("utf-8")
            if bcrypt.checkpw(encoded_password, encoded_hashed_password):
                return True
            else:
                return False
        except InvalidRequestError or NoResultFound:
            return False


def _hash_password(password: str) -> bytes:
    """method that takes in a password string arguments and returns bytes
    The returned bytes is a salted hash of the input password,
    hashed with bcrypt.hashpw"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """returns a string representation of a new UUID"""
    return str(uuid4())
