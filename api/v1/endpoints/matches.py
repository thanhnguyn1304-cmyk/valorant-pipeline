from fastapi import APIRouter, Depends
from sqlmodel import Session, select, delete
from typing import List

from backend.core.database import get_session  # Import hàm yield session xịn xò
from backend.models.match import Match  # Import Model
from backend.services.match_service import MatchService


router = APIRouter()


@router.get("/{region}/{puuid}")
async def get_matches(region: str, puuid: str):
    match_service = MatchService()
    return await match_service.get_matches_by_region_and_puuid(region, puuid)


@router.get("/", response_model=List[Match])
def get_all_matches(db: Session = Depends(get_session)):
    # 1. Check DB
    statement = select(Match)
    matches_in_db = db.exec(statement).all()

    if matches_in_db:
        print("Data found in pantry. Returning fast")
        return matches_in_db

    # 2. Nếu DB trống -> Tạo Mock Data
    else:
        print("Pantry empty. Cooking up fresh matches...")
        mock_matches = [
            Match(
                agentName="Sova",
                mapName="Pearl",
                roundsWon="10",
                roundsLost="13",
                score="10 - 13",
                kda="17/18/1",
                kdRatio="0.9",
                isWin=False,
                position="8th",
                hsPercent="42",
                adr="109",
                acs="186",
            ),
            Match(
                agentName="Clove",
                mapName="Haven",
                roundsWon="9",
                roundsLost="13",
                score="9 - 13",
                kda="20/19/14",
                kdRatio="1.1",
                isWin=False,
                position="3rd",
                hsPercent="29",
                adr="180",
                acs="283",
            ),
            Match(
                agentName="Clove",
                mapName="Bind",
                roundsWon="8",
                roundsLost="13",
                score="8 - 13",
                kda="16/18/6",
                kdRatio="0.9",
                isWin=False,
                position="6th",
                hsPercent="48",
                adr="143",
                acs="215",
            ),
            Match(
                agentName="Clove",
                mapName="Corrode",
                roundsWon="13",
                roundsLost="11",
                score="13 - 11",
                kda="29/21/8",
                kdRatio="1.4",
                isWin=True,
                position="MVP",
                hsPercent="36",
                adr="216",
                acs="333",
            ),
            # Add more rows here if you want!
        ]
        for match in mock_matches:
            db.add(match)
        db.commit()

        for match in mock_matches:
            db.refresh(match)

        return mock_matches


@router.post("/refresh")
def refresh_matches_cache(db: Session = Depends(get_session)):
    # Xóa toàn bộ
    statement = delete(Match)
    db.exec(statement)
    db.commit()
    return {"message": "Cache is cleared. Pantry is now empty"}
