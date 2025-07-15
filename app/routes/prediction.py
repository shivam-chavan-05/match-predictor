from fastapi import APIRouter, Depends, Header, HTTPException
from app.database import predictions, users
from app.utils.jwt import decode_token
from pydantic import BaseModel

router = APIRouter()

class Prediction(BaseModel):
    match_id: str
    prediction: str  # Expected values: "win", "draw", "lose"

def get_user(token: str = Header(...)):
    data = decode_token(token)  # Decodes JWT token and returns user info (assumed)
    user = users.find_one({"username": data["username"]})
    if not user:
        raise HTTPException(401, "Invalid user")
    return user

@router.post("/predict")
def predict(data: Prediction, user=Depends(get_user)):
    predictions.insert_one({
        "user_id": str(user["_id"]),
        "match_id": data.match_id,
        "prediction": data.prediction,
        "actual_result": None
    })
    return {"msg": "Prediction submitted"}

@router.get("/leaderboard")
def leaderboard():
    # Assuming users collection has 'username' and 'score' fields
    return list(users.find({}, {"username": 1, "score": 1, "_id": 0}))
