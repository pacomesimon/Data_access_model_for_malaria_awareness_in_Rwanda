from flask import request, jsonify
from db_models import *
import json

def authentication_function():
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