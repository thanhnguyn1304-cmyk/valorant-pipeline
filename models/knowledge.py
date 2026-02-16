from typing import Optional, List
from sqlmodel import SQLModel, Field
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column

class CoachingTip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    agent: str = "all"
    map_name: str = "all" 
    category: str
    # Gemini text-embedding-004 uses 768 dimensions
    embedding: List[float] = Field(sa_column=Column(Vector(768)))
