#!/usr/bin/env python3
"""module for SessionAuth class that handles
session authentication mechanism"""
from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """SessionAuth class for handling session authentication mechanism"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if isinstance(user_id, str):
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)
        return None
