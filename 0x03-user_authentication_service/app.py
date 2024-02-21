#!/usr/bin/env python3
"""basic Flask app"""
from auth import Auth
from flask import Flask, jsonify, request

app = Flask(__name__)

AUTH = Auth()


@app.route("/", methods=["GET"])
def index():
    """return a JSON payload of the form:
        {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """registers the user into the database"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
