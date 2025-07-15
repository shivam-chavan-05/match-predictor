from fastapi import APIRouter
from app.database import matches, cache_meta  # assuming you have another collection
import requests
import os
from datetime import datetime, timedelta


router = APIRouter()

@router.get("/matches")
def get_matches():
    # Retrieve cache metadata
    meta = cache_meta.find_one({"key": "matches_last_updated"})
    now = datetime.utcnow()
    cache_expired = True

    if meta:
        last_updated = meta["value"]
        # Check if last update is within last 24 hours
        if now - last_updated < timedelta(hours=24):
            cache_expired = False

    if matches.count_documents({}) == 0 or cache_expired:
        # Clear old cached matches
        matches.delete_many({})
        # Fetch fresh matches
        res = requests.get(f"https://www.thesportsdb.com/api/v1/json/{os.getenv('SPORTSDB_API_KEY')}/eventsnextleague.php?id=4328")
        events = res.json().get("events", [])
        for event in events:
            matches.insert_one({
                "match_id": event["idEvent"],
                "team1": event["strHomeTeam"],
                "team2": event["strAwayTeam"],
                "start_time": event["dateEvent"] + " " + event["strTime"],
                "result": None
            })
        # Update cache timestamp
        cache_meta.update_one(
            {"key": "matches_last_updated"},
            {"$set": {"value": now}},
            upsert=True
        )

    # Return all matches without MongoDB _id
    return list(matches.find({}, {"_id": 0}))
