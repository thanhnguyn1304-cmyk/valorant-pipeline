from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint
from typing import List, Optional
from datetime import datetime

class Match(SQLModel, table=True):
    id: str = Field(
        primary_key=True, index=True, unique=True
    )  # The Riot Match ID (e.g., "a7f3...")
    map_name: str
    start_time: datetime
    start_time_patched: str  # Unix timestamp (e.g., 1703650000)
    duration_ms: int  # Duration in milliseconds
    winning_team: str  # "Blue" or "Red"
    rounds_play : int

    blue_team_score: int
    red_team_score: int

    # THE RELATIONSHIP:
    # This says: "I have a list of players. Go look at the 'match' variable in the other table."
    participations: List["MatchParticipation"] = Relationship(back_populates="match")


class MatchParticipation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    match_id: str = Field(foreign_key="match.id", index=True)
    rounds_played: int
    start_time: datetime
    map : str
    user_id: str
    user_tag: str

    puuid: str = Field(index=True)
    agent_name: str
    agent_image: str

    team_id: str
    current_rank:str
    current_rank_image:str

    kills: int
    deaths: int
    assists: int

    combat_score: int
    headshots: int
    othershots: int

    damage_dealt: int
    damage_taken: int

    roundsWon : int
    roundsLost : int
    result : str
    position : int
    linked_to_match : bool = Field(default = False)

    match: Optional[Match] = Relationship(back_populates="participations")

    __table_args__ = (
        UniqueConstraint("match_id", "puuid", name="unique_match_participation"),
    )
