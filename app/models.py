UserSchema = {
    "username": str,
    "password": str,  # hashed
    "score": int
}

PredictionSchema = {
    "user_id": str,
    "match_id": str,
    "prediction": str,  # win/draw/lose
    "actual_result": str  # updated later
}

MatchSchema = {
    "match_id": str,
    "team1": str,
    "team2": str,
    "start_time": str,
    "result": str  # updated after completion
}
