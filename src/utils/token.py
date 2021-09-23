import jwt
import os
from datetime import datetime, timedelta
from flask import jsonify, abort

secretKey = "enc-amanojaku-putih"

def encode(data):
    payload = {
        "data" : data,
        "exp" : datetime.utcnow() + timedelta(days = 1),
        "iat" : datetime.utcnow()
    }
    
    # encoded = jwt.encode(payload,secretKey,algorithm="HS256").decode('utf-8')
    encoded = jwt.encode(payload,secretKey,algorithm="HS256")
    return encoded

def decode(data):
    try:
        decoded = jwt.decode(data,secretKey,algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        abort(403)
    except jwt.DecodeError:
        abort(403)
    return decoded