from fastapi import APIRouter, Depends
from sqlmodel import Session, select, delete, desc
from typing import List

from core.database import get_session  # Import hàm yield session xịn xò
from models.match import Match, MatchParticipation  # Import Model
from models.user import User
from services.match_service import MatchService
from schemas.match_schema import ParticipationBase, MatchScoreboard

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


@router.get("/{region}/{puuid}", response_model=List[ParticipationBase])
async def get_matches(region: str, puuid: str, db: Session = Depends(get_session)):

    match_service = MatchService()

    users_in_db = select(User).where(User.puuid == puuid)
    user_in_db = db.exec(users_in_db).first()

    if user_in_db:
        batch = 10
        start = 0
        while True:
            # Fetch matches from external API
            match_data = await match_service.get_matches_by_region_and_puuid(
                region, puuid, start
            )

            if not match_data:
                break

            # Process and save matches
            a = match_service.fetch_and_update_matches(match_data, puuid, db)

            start += batch

            # Safety break: Limit to 20 matches (2 batches)
            if start >= 20:
                break

            if a == "done":
                break

    else:
        for i in range(2):
            current_start = i * 10
            match_data = await match_service.get_matches_by_region_and_puuid(
                region, puuid, current_start
            )
            match_service.fetch_and_update_matches(match_data, puuid, db)
    statement = (
        select(MatchParticipation)
        .join(Match)
        .where(MatchParticipation.puuid == puuid)
        .order_by(desc(MatchParticipation.start_time))
        .limit(20)
    )

    matches = db.exec(statement).all()

    return matches


@router.get("/{match_id}", response_model=MatchScoreboard)
def get_match_by_id(match_id: str, db: Session = Depends(get_session)):

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
