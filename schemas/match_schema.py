from typing import List, Optional, Any
from sqlmodel import SQLModel
from backend.models.match import Match, MatchParticipation # Import your actual DB models
from pydantic import computed_field
# --- 1. BASIC BUILDING BLOCKS ---
# These define what data is "public" safe. 
# We usually inherit from SQLModel, but we DON'T add table=True.

class MatchBase(SQLModel):
    id: str
    map_name: str
    start_time: Any  # Can be datetime or int
    duration_ms: int
    winning_team: str
    rounds_play: int

class ParticipationBase(SQLModel):
    id : int
    match_id: str
    user_id : str
    user_tag : str
    agent_name: str
    map: str
    roundsWon : int
    roundsLost: int
    rounds_played: int
    start_time: Any  # datetime from backend
    team_id: str
    puuid: str
    kills: int
    deaths: int
    assists: int
    headshots: int
    othershots: int
    combat_score: int
    damage_dealt: int
    result: str
    position :int
    agent_image:str
    current_rank: str
    current_rank_image: str
    @computed_field
    def fmt_pos(self)-> str:
        if self.position == 1:
            fmt_pos = 'MVP'
        elif self.position == 2:
            fmt_pos = '2nd'
        elif self.position == 3:
            fmt_pos = '3rd'
        else:
            fmt_pos = f'{self.position}th'
        
        return fmt_pos
    @computed_field
    def adr(self) -> int:
        adr = round(self.damage_dealt / self.rounds_played)
        return adr
    @computed_field
    def acs(self) -> int:
        acs = round(self.combat_score / self.rounds_played)
        return acs
    @computed_field
    def hsPercent(self) -> int:
        hs = round((self.headshots / (self.headshots + self.othershots)) * 100)
        return hs
    # --- THE CALCULATED FIELDS ---
    @computed_field
    def kdRatio(self) -> float:
        if self.deaths == 0:
            return float(self.kills) # Avoid division by zero!
        a = round(self.kills / self.deaths, 2)
        return f'{a:.1f}'
    @computed_field
    def kda(self) -> str:
        # You can even format text strings!
        # Example output: "15 / 5 / 10"
        return f"{self.kills}/{self.deaths}/{self.assists}"

    # Add other stats like damage, headshots here if you want the frontend to see them

# --- 2. THE COMPOSITE SCHEMAS (What React actually gets) ---

# SCENARIO A: "My Match History"
# When showing a list of games, we are listing "Participations".
# But we need the Match info (Map, Time) inside it to show the card.
#class MatchHistoryCard(ParticipationBase):
    # This is the magic. We verify that the 'match' relationship 
    # gets converted into our MatchBase schema.
    

# SCENARIO B: "The Scoreboard"
# When showing one specific game, we start with the Match info,
# and we want a list of ALL players inside it.
class MatchScoreboard(MatchBase):
    participations: List[ParticipationBase]