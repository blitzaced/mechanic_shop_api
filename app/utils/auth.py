from datetime import datetime, timedelta, timezone
from jose import jwt
import jose
from functools import wraps
from flask import request, jsonify


SECRET_KEY = "super secret secrets"

def encode_token(customer_id):                                                  #using unique pieces of info to make our tokens user specific
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0,hours=1),          #Setting the expiration time to an hour past now
        'iat': datetime.now(timezone.utc),                                      #Issued at
        'sub':  str(customer_id)                                                #This needs to be a string or the token will be malformed and won't be able to be decoded.
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        auth_header = request.headers.get('Authorization', '')
        parts = auth_header.split()

        if len(parts) == 2 and parts[0] == 'Bearer':
            token = parts[1]
        else:
            return jsonify({'message': 'Token is missing or improperly formatted!'}), 400

        try:
            # Decode the token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            customer_id = data['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 400
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 400

        return f(customer_id, *args, **kwargs)
        
    return decorated