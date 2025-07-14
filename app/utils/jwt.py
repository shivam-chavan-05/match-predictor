from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
SECRET = os.getenv("JWT_SECRET")

def create_token(data: dict):
    data["exp"] = datetime.utcnow() + timedelta(hours=3)
    return jwt.encode(data, SECRET, algorithm="HS256")

def decode_token(token: str):
    return jwt.decode(token, SECRET, algorithms=["HS256"])