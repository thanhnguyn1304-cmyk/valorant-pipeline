from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select, delete, desc
from typing import List

from core.database import get_session  # Import hàm yield session xịn xò
from models.match import Match, MatchParticipation  # Import Model
from models.user import User
from services.match_service import MatchService
from schemas.match_schema import ParticipationBase, MatchScoreboard
from core.limiter import limiter

router = APIRouter()


@router.get("/demo/{region}/{puuid}")
async def demo(region: str, puuid: str):
    match_service = MatchService()

    match_data = await match_service.get_matches_by_region_and_puuid(region, puuid, 0)
    return match_data


@router.get("/demo2/{puuid}", response_model=List[ParticipationBase])
async def demo2(puuid: str, db: Session = Depends(get_session)):

    statement = (
        select(MatchParticipation)
        .where(MatchParticipation.puuid == puuid)
        .order_by(desc(MatchParticipation.start_time))
    )
    matches = db.exec(statement).all()
    return matches


import json
import redis
from celery.result import AsyncResult
from core.config import settings
from worker import celery_app, fetch_matches_task

# Initialize Redis connection for caching
redis_client = redis.Redis.from_url(settings.REDIS_URL.replace("redis://", "redis://"), decode_responses=True)

@router.get("/{region}/{puuid}", response_model=List[ParticipationBase])
@limiter.limit("30/minute")
async def get_matches(request: Request, region: str, puuid: str, db: Session = Depends(get_session)):
    
    # 1. Check Redis Cache
    cache_key = f"player_matches_{puuid}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    # 2. If not in cache, query DB
    statement = (
        select(MatchParticipation)
        .join(Match)
        .where(MatchParticipation.puuid == puuid)
        .order_by(desc(MatchParticipation.start_time))
        .limit(20)
    )

    matches = db.exec(statement).all()
    
    # Check if we should create a placeholder user (Smart Sync optimization)
    if len(matches) == 0:
        users_in_db = select(User).where(User.puuid == puuid)
        user_in_db = db.exec(users_in_db).first()
        if not user_in_db:
             new_user = User(puuid=puuid, region=region, user_id="Unknown", user_tag="Unknown")
             db.add(new_user)
             db.commit()

    # 3. Store in Redis cache for 5 minutes (300 seconds)
    if matches:
        from schemas.match_schema import ParticipationBase
        from fastapi.encoders import jsonable_encoder
        
        # Convert the raw database models into our clean Pydantic schema first!
        # This strips the cyclic Match -> Participation relationship that crashes jsonable_encoder
        safe_matches = [ParticipationBase.model_validate(m) for m in matches]
        matches_dict = jsonable_encoder(safe_matches)
        
        redis_client.setex(cache_key, 300, json.dumps(matches_dict))

    return matches


@router.post("/{region}/{puuid}/update")
@limiter.limit("5/minute")
def trigger_match_update(request: Request, region: str, puuid: str):
    """
    Triggers the background Celery task to fetch the latest matches.
    """
    task = fetch_matches_task.delay(puuid, region)
    return {"task_id": task.id, "status": "processing"}


@router.get("/update/status/{task_id}")
def get_update_status(task_id: str):
    """
    Poll this endpoint to get the status of the background update task.
    """
    task = AsyncResult(task_id, app=celery_app)
    
    response = {
        "state": task.state,
    }
    
    if task.state == 'PROGRESS':
        response["meta"] = task.info
    elif task.state == 'SUCCESS':
        response["meta"] = task.result
    elif task.state == 'FAILURE':
        response["meta"] = str(task.info)
        
    return response


@router.get("/{match_id}", response_model=MatchScoreboard)
@limiter.limit("60/minute")
def get_match_by_id(request: Request, match_id: str, db: Session = Depends(get_session)):

    match_service = MatchService()

    match_detail = match_service.get_match_detail(match_id, db)

    return match_detail


# @router.get("/", response_model=List[Match])
# def get_all_matches(db: Session = Depends(get_session)):


@router.post("/refresh")
def refresh_matches_cache(db: Session = Depends(get_session)):
    # Xóa toàn bộ
    statement1 = delete(MatchParticipation)
    db.exec(statement1)

    # 2. Delete the Parents (Matches) SECOND
    statement2 = delete(Match)
    db.exec(statement2)
    db.commit()
    return {"message": "Cache is cleared. Pantry is now empty"}

