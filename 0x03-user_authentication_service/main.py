#!/usr/bin/env python3
"""tests for user authentication"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """test registering user"""
    body = {
        "email": email,
        "password": password
    }
    res = requests.post(f"{URL}/users", data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}
    res = requests.post(f"{URL}/users", data=body)
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """test login with wrong password"""
    body = {
        "email": email,
        "password": password
    }
    res = requests.post(f"{URL}/sessions", data=body)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """test login"""
    body = {
        "email": email,
        "password": password
    }
    res = requests.post(f"{URL}/sessions", data=body)
    assert res.json() == {"email": email, "message": "logged in"}
    assert res.status_code == 200
    return res.cookies.get("session_id")


def profile_unlogged() -> None:
    """test getting profile data while ulogged"""
    res = requests.get(f"{URL}/profile")
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """test getting profile data while logged in"""
    res = requests.get(f"{URL}/profile", cookies={"session_id": session_id})
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """test logout"""
    res = requests.delete(f"{URL}/sessions",
                          cookies={"session_id": session_id})
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """test reset password token"""
    body = {
        "email": email
    }
    res = requests.post(f"{URL}/reset_password", data=body)
    assert res.status_code == 200
    reset_token = res.json().get("reset_token")
    assert res.json() == {"email": email, "reset_token": reset_token}
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """test update password"""
    body = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    res = requests.put(f"{URL}/reset_password", data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
