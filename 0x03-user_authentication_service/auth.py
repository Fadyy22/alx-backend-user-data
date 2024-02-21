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
            self._db.find_user_by(email=email)
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

    def create_session(self, email: str) -> str:
        """generates a new UUID and store it in the database
        as the user’s session_id, then return the session ID"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except InvalidRequestError or NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """return user by session_id if found, else None"""
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except InvalidRequestError or NoResultFound:
                return None
        return None

    def destroy_session(self, user_id: int) -> None:
        """updates the corresponding user’s session ID to None"""
        try:
            self._db.update_user(user_id, session_id=None)
        except InvalidRequestError or NoResultFound:
            return None


def _hash_password(password: str) -> bytes:
    """method that takes in a password string arguments and returns bytes
    The returned bytes is a salted hash of the input password,
    hashed with bcrypt.hashpw"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """returns a string representation of a new UUID"""
    return str(uuid4())
