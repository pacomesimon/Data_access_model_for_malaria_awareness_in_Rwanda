#!/usr/bin/env python
"""The Authentication function source code
DESCRIPTION:
------------
This file contains the authentication function source code."""

from flask import request, jsonify
from db_models import *
import json

def authentication_function():
    """
    Authenticate a user based on provided credentials in the request headers.

    Returns:
        dict: A dictionary containing authentication response and error status.
              If authentication is successful, returns user details and sets "error" to False.
              If authentication fails due to bad/no credentials, bad email, or incorrect password,
              sets "error" to True and provides an appropriate response.
    """
    try:
        creds_dict = json.loads(request.headers.get('Authorization'))
    except:
        return ({"error": True, "response":"bad/no auth credentials"})
    try:
        user_details = User.query.filter_by(email=creds_dict["email"]).first()
    except:
        return ({"error": True, "response":"bad email or password"})
    try:
        assert creds_dict["password"] == user_details.password
    except:
        return ({"error": True, "response":"bad email or password"})
    
    return {"response": user_details, "error": False}