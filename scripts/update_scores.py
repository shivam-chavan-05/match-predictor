from app.database import matches, predictions, users
import requests
import os

def update_results():
    for match in matches.find({"result": None}):

        res = requests.get(f"https://www.thesportsdb.com/api/v1/json/{os.getenv('SPORTSDB_API_KEY')}/lookupevent.php?id={match['match_id']}")
        

        event = res.json().get("events", [None])[0]
        

        if not event or not event.get("intHomeScore"):
            continue
        
   
        home = int(event["intHomeScore"])
        away = int(event["intAwayScore"])
        
        result = "win" if home > away else "lose" if away > home else "draw"
        
        matches.update_one({"match_id": match["match_id"]}, {"$set": {"result": result}})
        

        for pred in predictions.find({"match_id": match["match_id"]}):
            predictions.update_one({"_id": pred["_id"]}, {"$set": {"actual_result": result}})
            
            if pred["prediction"] == result:
                users.update_one({"_id": pred["user_id"]}, {"$inc": {"score": 3}})
