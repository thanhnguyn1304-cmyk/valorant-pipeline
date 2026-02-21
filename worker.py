import os
from celery import Celery
from core.config import settings
from sqlmodel import Session
from core.database import engine
import time

# Create the Celery app
celery_app = Celery(
    "valortracker_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

import asyncio
from services.match_service import MatchService

@celery_app.task(bind=True)
def fetch_matches_task(self, puuid: str, region: str):
    """
    Background task to fetch matches from Riot API and store them.
    """
    self.update_state(state="PROGRESS", meta={"status": "Fetching from Riot API...", "current": 0, "total": 20})
    
    match_service = MatchService()
    
    # We will fetch 20 matches.
    batch = 20
    start = 0
    
    # Async call to external API needs to be run in event loop
    try:
        match_data = asyncio.run(match_service.get_matches_by_region_and_puuid(region, puuid, start))
        
        if not match_data:
            return {"status": "Complete", "message": "No matches found."}
            
        self.update_state(state="PROGRESS", meta={"status": "Processing and saving matches to database...", "current": 10, "total": 20})
        
        # Save to DB
        with Session(engine) as db:
            match_service.fetch_and_update_matches(match_data, puuid, db)
            
        # Clean up the Redis cache for this user so they get fresh data next time
        import redis
        r = redis.Redis.from_url(settings.REDIS_URL.replace("redis://", "redis://"))
        r.delete(f"player_matches_{puuid}")
            
    except Exception as e:
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise e
        
    return {"status": "Complete", "message": f"Successfully fetched matches."}
