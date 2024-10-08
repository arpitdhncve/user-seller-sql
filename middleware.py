from lib2to3.pgen2 import token
from dotenv import load_dotenv
import os
from datetime import datetime , timedelta
import jwt
from redishandler import get_token


load_dotenv()

secret_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')


def create_jwt(email):
    try:
        payload = {
            'email' : email,
            'exp' : datetime.utcnow() + timedelta(minutes=30)
        }

        token = jwt.encode(payload, secret_key, algorithm= algorithm)

        return token

    except Exception as e:
        
        print(f"error incCreating JWT Token : {e}")
        return None



def decode_jwt(token):
    print(token)
    try:
        decode = jwt.decode(str(token), secret_key, algorithms = [algorithm])

        email = decode.get('email')
        exp = datetime.utcfromtimestamp(decode.get('exp'))

        return {
            "email" : email,
            "exp" : exp
        }

    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid Token")
        return None
    except Exception as e:
        print(f"Error in decoding JWT Token: {e}")
        return None




def check_authorization(email, authorization):
    if authorization is None or not authorization.startswith("Bearer "):
        return "auth token missing", False
    
    else:
        actual_token = authorization[7:]
        token_in_redis = get_token(email)
        if token_in_redis is None:
            return "Session expired, login again", False

        if actual_token ==  token_in_redis:
            payload = decode_jwt(actual_token)

            if payload is None:
                return "Session expired, login again", False

            if payload["email"] == email:
                return "User is authorized", True
            else:
                return "Token and user are not same", False

