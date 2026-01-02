import httpx
from backend.core.config import settings
from fastapi import HTTPException
from backend.models.match import Match, MatchParticipation
from sqlmodel import Session, select



class MatchService:
    def __init__(self):
        self.base_url = "https://api.henrikdev.xyz/valorant"
        self.headers = {"Authorization": settings.ACCESS_TOKEN, "Accept": "*/*"}
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(10.0))

    async def get_matches_by_region_and_puuid(self, region: str, puuid: str):
        url = self.base_url + f"/v3/by-puuid/matches/{region}/{puuid}?mode=competitive&size=2"
        async with self.client as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                match_data = data['data']
                return match_data


            error_msg = f"HenrikAPI Error: {response.status_code} - {response.text}"
            print(error_msg)  # In ra terminal (phòng hờ)
            raise HTTPException(status_code=response.status_code, detail=error_msg)
        
    async def fetch_and_update_matches(self, match_data, puuid, db: Session):
        for match_json in match_data:
            match_id = match_json["metadata"]["matchId"]
            statement = select(Match).where(Match.id == match_id)
            match_in_db = db.exec(statement).first()
            if match_in_db :
                continue
            else:
                new_match = Match(
                    id=match_id,
                    map_name=match_json["metadata"]["map"],
                    start_time=match_json["metadata"]["game_start_patched"],
                    duration_ms=match_json["metadata"]["game_length"],
                    winning_team = 'red' if match_json["teams"]["red"]["has_won"] else 'blue', # "Blue" or "Red"
                    rounds_play = match_json["metadata"]["rounds_played"]







        matches_in_db = db.exec(select(Match)).all()
        
        for match in match_data:

            
            match_id = match["metadata"]["matchId"]

        
