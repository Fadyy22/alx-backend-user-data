#!/usr/bin/env python3
"""module for encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns salted and hashed password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
