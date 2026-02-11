from fastapi import APIRouter
from services.riot_client import RiotClient
from services.player_service import PlayerService
from fastapi import APIRouter, Depends
from sqlmodel import Session
from core.database import get_session

router = APIRouter()


@router.get("/{player_name}/{player_tag}")
async def get_player_info(player_name: str, player_tag: str, db: Session = Depends(get_session)):
    service = PlayerService()

    puuid, region = await service.get_player_info(player_name, player_tag, db)

    return {
        "puuid": puuid,
        "region": region,
    }


# blazinho : f31ce9ad-d4da-53dd-a902-c3e206299a6c
