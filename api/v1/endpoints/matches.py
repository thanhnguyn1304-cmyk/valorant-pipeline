from fastapi import APIRouter, Depends
from sqlmodel import Session, select, delete, desc
from typing import List

from backend.core.database import get_session  # Import hàm yield session xịn xò
from backend.models.match import Match, MatchParticipation  # Import Model
from backend.services.match_service import MatchService
from backend.schemas.match_schema import ParticipationBase

router = APIRouter()


@router.get("/{region}/{puuid}", response_model=List[ParticipationBase])
async def get_matches(region: str, puuid: str, db: Session = Depends(get_session)):
    match_service = MatchService()
    match_data =  await match_service.get_matches_by_region_and_puuid(region, puuid)

    match_service.fetch_and_update_matches(match_data, puuid,db)

    statement = select(MatchParticipation).join(Match).where(MatchParticipation.puuid == puuid).order_by(desc(MatchParticipation.start_time))

    matches = db.exec(statement).all()

    return matches



#@router.get("/", response_model=List[Match])
#def get_all_matches(db: Session = Depends(get_session)):
    

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
