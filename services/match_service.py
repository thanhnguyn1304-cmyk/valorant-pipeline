import httpx
from backend.core.config import settings
from fastapi import HTTPException
from backend.models.match import Match, MatchParticipation
from sqlmodel import Session, select
from datetime import datetime
from backend.assets.agent_icon import small_display_icon


class MatchService:
    def __init__(self):
        self.base_url = "https://api.henrikdev.xyz/valorant"
        self.headers = {"Authorization": settings.ACCESS_TOKEN, "Accept": "*/*"}

    async def get_matches_by_region_and_puuid(
        self, region: str, puuid: str, start: int
    ):
        url = (
            self.base_url
            + f"/v4/by-puuid/matches/{region}/pc/{puuid}?mode=competitive&size=10&start={start}"
        )
        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                match_data = data["data"]
                return match_data

            error_msg = f"HenrikAPI Error: {response.status_code} - {response.text}"
            print(error_msg)  # In ra terminal (phòng hờ)
            raise HTTPException(status_code=response.status_code, detail=error_msg)

    def update_player_link(self, match_id: str, puuid: str, db: Session):
        statement = select(MatchParticipation).where(
            MatchParticipation.match_id == match_id, MatchParticipation.puuid == puuid
        )
        participation_in_db = db.exec(statement).first()
        if participation_in_db:
            participation_in_db.linked_to_match = True
            db.commit()
            db.refresh(participation_in_db)

    def fetch_and_update_matches(self, match_data, puuid: str, db: Session):
        k = 3
        for match_json in match_data:
            match_id = match_json["metadata"]["match_id"]
            statement = select(Match).where(Match.id == match_id)
            match_in_db = db.exec(statement).first()
            if match_in_db:
                stmt = select(MatchParticipation).where(
                    MatchParticipation.match_id == match_id,
                    MatchParticipation.puuid == puuid,
                )

                participation = db.exec(stmt).first()

                if participation and participation.linked_to_match:
                    k -= 1
                    if k == 0:
                        return "done"  # Safety cap of 3 we stop here
                else:
                    self.update_player_link(match_id, puuid, db)
                    k = 3

            else:
                new_match = Match(
                    id=match_id,
                    map_name=match_json["metadata"]["map"]["name"],
                    start_time=match_json["metadata"]["started_at"],
                    start_time_patched=datetime.fromisoformat(match_json["metadata"]["started_at"]),
                    duration_ms=match_json["metadata"]["game_length_in_ms"],
                    winning_team=(
                        "Red" if match_json["teams"][0]["won"] else "Blue"
                    ),  # "Blue" or "Red"
                    rounds_play=match_json["teams"][0]["rounds"]["won"]+match_json["teams"][0]["rounds"]["lost"],
                    blue_team_score=match_json["teams"][1]["rounds"]["won"],
                    red_team_score=match_json["teams"][0]["rounds"]["won"],
                )
                db.add(new_match)
                db.commit()
                db.refresh(new_match)

                all_players_raw = match_json["players"]

                all_players_sorted = sorted(
                    all_players_raw, key=lambda x: x["stats"]["score"], reverse=True
                )

                # 3. LOOP WITH INDEX (enumerate gives us the rank automatically)
                # start=1 means the first person is #1, not #0
                participations_to_add = []
                for rank, players in enumerate(all_players_sorted, start=1):
                    if new_match.blue_team_score == new_match.red_team_score:
                        tmpres = "draw"
                    elif (
                        new_match.blue_team_score > new_match.red_team_score
                        and players["team_id"] == "Blue"
                    ):
                        tmpres = "win"
                    elif (
                        new_match.blue_team_score < new_match.red_team_score
                        and players["team_id"] == "Red"
                    ):
                        tmpres = "win"
                    else:
                        tmpres = "lose"
                        
                    new_participation = MatchParticipation(
                        match_id=new_match.id,
                        rounds_played=new_match.rounds_play,
                        start_time=new_match.start_time,
                        map=new_match.map_name,
                        user_id=players["name"],
                        user_tag=players["tag"],
                        puuid=players["puuid"],
                        agent_name=players["agent"]["name"],
                        agent_image=small_display_icon[players["agent"]["name"]],
                        
                        team_id=players["team_id"],
                        current_rank=players["tier"]["name"],
                        current_rank_image=f"/static/rank_png/{players['tier']['name']}.png" if players.get("tier", {}).get("name") else "",
                        kills=players["stats"]["kills"],
                        deaths=players["stats"]["deaths"],
                        assists=players["stats"]["assists"],
                        combat_score=players["stats"]["score"],
                        headshots=players["stats"]["headshots"],
                        othershots=players["stats"]["bodyshots"]
                        + players["stats"]["legshots"],
                        damage_dealt=players["stats"]["damage"]["dealt"],
                        damage_taken=players["stats"]["damage"]["received"],
                        roundsWon=(
                            new_match.blue_team_score
                            if players["team_id"] == "Blue"
                            else new_match.red_team_score
                        ),
                        roundsLost=(
                            new_match.red_team_score
                            if players["team_id"] == "Blue"
                            else new_match.blue_team_score
                        ),
                        result=tmpres,
                        position=rank,
                        linked_to_match=True if players["puuid"] == puuid else False,
                    )
                    participations_to_add.append(new_participation)
                
                # Bulk insert all participations for this match
                db.add_all(participations_to_add)
                db.commit()
            
    def get_match_detail(self, match_id: str, db : Session):
        # Query match details with participations
        statement = select(Match).where(Match.id == match_id)
        match = db.exec(statement).first()

        if not match:
            return None

        # Query participations by match_id
        statement = select(MatchParticipation).where(MatchParticipation.match_id == match_id)
        participants = db.exec(statement).all()

        # Set participations on the match object
        match.participations = participants

        return match

