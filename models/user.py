from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class User(SQLModel, table=True):
    __tablename__ = "users"
    puuid: str = Field(default=None, primary_key=True, unique = True, index = True)
    user_id : str
    user_tag : str
    region : str



    
                            