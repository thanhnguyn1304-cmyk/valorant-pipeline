from fastapi import APIRouter, Depends
from sqlmodel import Session, select, delete
from typing import List
import httpx
import json
from core.database import get_session  # Import hàm yield session xịn xò
from models.agent import Agent  # Import Model
router = APIRouter()
from services.agent_service import AgentService


@router.get("/", response_model=List[Agent])
async def get_all_agents(db: Session = Depends(get_session)):
    return await AgentService.fecth_and_update_agents(db)

# done with the update part in CRUD, now we go to the delete part


@router.post("/refresh")
def refresh_agents_cache(db: Session = Depends(get_session)):
    statement = delete(Agent)
    # deleting everything, can add where(Agent.displayName == "Jett")), delete(Agent)
    db.exec(statement)
    db.commit()
    return "Cache is cleared. Pantry is now empty"
