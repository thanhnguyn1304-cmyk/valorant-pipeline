from sqlmodel import SQLModel, Field


class Match(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    agentName: str
    mapName: str
    score: str
    roundsWon: str
    roundsLost: str
    kda: str
    kdRatio: str
    isWin: bool
    position: str
    hsPercent: int
    adr: int
    acs: int
