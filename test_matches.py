import json
import asyncio
from schemas.match_schema import ParticipationBase
from models.match import MatchParticipation
from fastapi.encoders import jsonable_encoder

m = MatchParticipation(
    id=1,
    match_id="test_match_id",
    rounds_played=10,
    start_time="2023-01-01T00:00:00",
    map="Bind",
    user_id="test",
    user_tag="test",
    puuid="test",
    agent_name="Jett",
    agent_image="url",
    team_id="Blue",
    current_rank="Gold",
    current_rank_image="url",
    kills=10,
    deaths=10,
    assists=10,
    combat_score=100,
    headshots=10,
    othershots=10,
    damage_dealt=1000,
    damage_taken=1000,
    roundsWon=5,
    roundsLost=5,
    result="Draw",
    position=1
)

print("model_validate...")
try:
    safe_m = ParticipationBase.model_validate(m)
    print("validate success")
    d = jsonable_encoder(safe_m)
    print("encoder success:", d)
except Exception as e:
    import traceback
    traceback.print_exc()
