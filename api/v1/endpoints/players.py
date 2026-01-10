from fastapi import APIRouter
from backend.services.riot_client import RiotClient
from backend.services.player_service import PlayerService

router = APIRouter()


@router.get("/{player_name}/{player_tag}")
async def get_player_info(player_name: str, player_tag: str):
    service = PlayerService

    puuid, region = await service.get_puuid_and_region(player_name, player_tag)

    return {
        "puuid": puuid,
        "region": region,
    }


# blazinho : f31ce9ad-d4da-53dd-a902-c3e206299a6c
