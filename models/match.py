from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class Match(SQLModel, table=True):
    id: str = Field(primary_key=True)  # The Riot Match ID (e.g., "a7f3...")
    map_name: str
    start_time: int  # Unix timestamp (e.g., 1703650000)
    duration_ms: int  # Duration in milliseconds
    winning_team: str  # "Blue" or "Red"
    rounds_play : int
    # THE RELATIONSHIP:
    # This says: "I have a list of players. Go look at the 'match' variable in the other table."
    participations: List["MatchParticipation"] = Relationship(back_populates="match")


class MatchParticipation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    match_id: str = Field(foreign_key="match.id")

    rounds_played: int = Field(foreign_key="match.rounds_play")

    puuid: str
    agent_name: str
    team_id: str
    current_rank:str
    kills: int
    deaths: int
    assists: int
    acs : int
    headshots: int
    othershots: int

    damage_dealt: int
    damage_taken: int

    match: Optional[Match] = Relationship(back_populates="participations")
