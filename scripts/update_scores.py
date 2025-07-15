from app.database import matches, predictions, users
import requests
import os

def update_results():
    # Loop over all matches where the result is not yet known
    for match in matches.find({"result": None}):
        # Call the sports API to get the latest event details by match_id
        res = requests.get(f"https://www.thesportsdb.com/api/v1/json/{os.getenv('SPORTSDB_API_KEY')}/lookupevent.php?id={match['match_id']}")
        
        # Extract event info from the API response JSON
        event = res.json().get("events", [None])[0]
        
        # If event data missing or no score info yet, skip this match for now
        if not event or not event.get("intHomeScore"):
            continue
        
        # Convert home and away scores from strings to integers
        home = int(event["intHomeScore"])
        away = int(event["intAwayScore"])
        
        # Determine match result from the scores: 'win', 'lose', or 'draw'
        result = "win" if home > away else "lose" if away > home else "draw"
        
        # Update the match document in the DB with the result
        matches.update_one({"match_id": match["match_id"]}, {"$set": {"result": result}})
        
        # For each prediction for this match:
        for pred in predictions.find({"match_id": match["match_id"]}):
            # Update the prediction document with the actual result
            predictions.update_one({"_id": pred["_id"]}, {"$set": {"actual_result": result}})
            
            # If the user's prediction was correct, increment their score by 3
            if pred["prediction"] == result:
                users.update_one({"_id": pred["user_id"]}, {"$inc": {"score": 3}})
