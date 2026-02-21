"""
CoachingTip model — stores coaching content with pgvector embeddings.
"""
from typing import Optional
from sqlmodel import SQLModel, Field, Column
from pgvector.sqlalchemy import Vector


class CoachingTip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    agent: str            # agent name or "all"
    map_name: str         # map name or "all"
    category: str         # e.g. "aim", "positioning", "economy"
    embedding: list[float] = Field(sa_column=Column(Vector(3072)))
