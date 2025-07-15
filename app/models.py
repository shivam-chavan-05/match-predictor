UserSchema = {
    "username": str,
    "password": str,  
    "score": int
}

PredictionSchema = {
    "user_id": str,
    "match_id": str,
    "prediction": str,  
    "actual_result": str  
}

MatchSchema = {
    "match_id": str,
    "team1": str,
    "team2": str,
    "start_time": str,
    "result": str  
}
