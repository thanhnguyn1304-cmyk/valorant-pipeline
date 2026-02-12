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

    # Smart Sync Optimization:
    # If user comes from a direct link/bookmark and isn't in DB yet,
    # create them so we can use the efficient sync logic below.
    if not user_in_db:
        # Create placeholder user
        new_user = User(
            puuid=puuid,
            region=region,
            user_id="Unknown",  # Will be updated next time they search or specific endpoint called
            user_tag="Unknown"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user_in_db = new_user

    # Now we ALWAYS enter the efficient block because user_in_db is guaranteed true
    if user_in_db:
        batch = 20 # Increased batch size slightly
        start = 0
        while True:
            # Fetch matches from external API
            match_data = await match_service.get_matches_by_region_and_puuid(
                region, puuid, start=start
            )

            if not match_data:
                break

            # Process and save matches
            # fetch_and_update_matches returns "done" if it hits existing matches
            status = match_service.fetch_and_update_matches(match_data, puuid, db)

            if status == "done":
                break
            
            start += batch
            # Safety break: Limit strictly to 20 recent matches for speed
            # The "Smart Sync" relies on hitting "done" early.
            # If it's a new user, we fetch 20. If existing capabilities, likely less.
            if start >= 20: 
                break

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
