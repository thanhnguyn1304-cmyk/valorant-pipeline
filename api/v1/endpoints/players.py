from fastapi import APIRouter
from backend.services.riot_client import RiotClient

router = APIRouter()


@router.get("/{player_name}/{player_tag}")
async def get_player_info(player_name: str, player_tag: str):
    client = RiotClient()

    puuid, region = await client.get_puuid_and_region(player_name, player_tag)

    return {
        "game_name": player_name,
        "tag_line": player_tag,
        "puuid": puuid,
        "region": region,
    }
