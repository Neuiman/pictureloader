import time
import jwt
from src.config import Settings

JWT_SECRET = Settings.JWT_SECRET
JWT_ALGORITHM = Settings.JWT_ALGORITHM


def token_response(token:str):
    return{
        "access_token": token
    }


def sign_jwt(email: str) -> str:
    payload = {
        "user_email": email,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
