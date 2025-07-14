from fastapi import APIRouter, HTTPException
from app.database import users
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt import create_token
from pydantic import BaseModel

router = APIRouter()

class Register(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: Register):
    if users.find_one({"username": user.username}):
        raise HTTPException(400, "Username already exists")
    users.insert_one({
        "username": user.username,
        "password": hash_password(user.password),
        "score": 0
    })
    return {"msg": "User registered"}

@router.post("/login")
def login(user: Register):
    db_user = users.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(401, "Invalid credentials")
    token = create_token({"username": user.username})
    return {"token": token}