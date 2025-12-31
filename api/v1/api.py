from fastapi import APIRouter
from backend.api.v1.endpoints import agents, matches, players

api_router = APIRouter()

api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(matches.router, prefix="/matches", tags=["matches"])
api_router.include_router(players.router, prefix="/players", tags=["players"])
