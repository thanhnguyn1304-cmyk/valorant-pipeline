from sqlmodel import SQLModel, Field

class Agent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    displayName: str
    role: str
    description: str
    displayIcon: str