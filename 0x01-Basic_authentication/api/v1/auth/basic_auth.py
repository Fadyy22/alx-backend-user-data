#!/usr/bin/env python3
"""module for BasicAuth class that handles authentication"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class for handling authentication"""
    pass
