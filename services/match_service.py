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
        url = self.base_url + f"/v3/by-puuid/matches/{region}/{puuid}?mode=competitive&size=10"
        async with self.client as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                match_data = data['data']
                return match_data

            error_msg = f"HenrikAPI Error: {response.status_code} - {response.text}"
            print(error_msg)  # In ra terminal (phòng hờ)
            raise HTTPException(status_code=response.status_code, detail=error_msg)

    def fetch_and_update_matches(self, match_data, puuid, db=Session):
        for match_json in match_data:
            match_id = match_json["metadata"]["matchid"]
            statement = select(Match).where(Match.id == match_id)
            match_in_db = db.exec(statement).first()
            if match_in_db :
                continue
            else:
                new_match = Match(
                    id=match_id,
                    map_name=match_json["metadata"]["map"],
                    start_time=match_json["metadata"]["game_start"],
                    start_time_patched=match_json["metadata"]["game_start_patched"],
                    duration_ms=match_json["metadata"]["game_length"],
                    winning_team=(
                        "red" if match_json["teams"]["red"]["has_won"] else "blue"
                    ),  # "Blue" or "Red"
                    rounds_play=match_json["metadata"]["rounds_played"],
                    blue_team_score = match_json['teams']['blue']['rounds_won'],
                    red_team_score = match_json['teams']['red']['rounds_won'],

                )
                db.add(new_match)
                db.commit()
                db.refresh(new_match)

                all_players_raw = match_json["players"]["all_players"]

                # 2. SORT THEM (Highest Combat Score First)
                # We use a 'lambda' to tell Python: "Sort using the 'score' inside 'stats'"
                all_players_sorted = sorted(
                    all_players_raw, 
                    key=lambda x: x["stats"]["score"], 
                    reverse=True
                )

                # 3. LOOP WITH INDEX (enumerate gives us the rank automatically)
                # start=1 means the first person is #1, not #0
                for rank, players in enumerate(all_players_sorted, start=1):
                    if new_match.blue_team_score == new_match.red_team_score:
                        tmpres = 'draw'
                    elif new_match.blue_team_score > new_match.red_team_score and players["team"] == 'Blue':
                        tmpres = 'win'
                    elif new_match.blue_team_score < new_match.red_team_score and players["team"] == 'Red':
                        tmpres = 'win'
                    else:
                        tmpres = 'lose'
                    new_participation = MatchParticipation(
                        match_id=new_match.id,
                        rounds_played=new_match.rounds_play, 
                        start_time=new_match.start_time,
                        map = new_match.map_name,
                        user_id=players["name"],
                        user_tag=players["tag"],
                        puuid=players["puuid"],
                        agent_name=players["character"],
                        agent_image=players["assets"]['agent']['small'],
                        team_id=players["team"],
                        current_rank=players["currenttier_patched"],
                        kills=players["stats"]["kills"],
                        deaths=players["stats"]["deaths"],
                        assists=players["stats"]["assists"],
                        combat_score=players["stats"]["score"],
                        headshots=players["stats"]["headshots"],
                        othershots=players["stats"]["bodyshots"]
                        + players["stats"]["legshots"],
                        damage_dealt=players["damage_made"],
                        damage_taken=players["damage_received"],
                        
                        roundsWon = new_match.blue_team_score if players["team"] == "Blue" else new_match.red_team_score,
                        roundsLost = new_match.red_team_score if players["team"] == "Blue" else new_match.blue_team_score,

                        result = tmpres,
                        position=rank,
                    ) 

                    db.add(new_participation)
                    db.commit()
                    db.refresh(new_participation)
