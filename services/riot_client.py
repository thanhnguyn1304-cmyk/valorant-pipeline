import httpx
from backend.core.config import settings
from fastapi import HTTPException


class RiotClient:
    def __init__(self):
        self.base_url = "https://api.henrikdev.xyz/valorant"
        self.headers = {"Authorization": settings.ACCESS_TOKEN, "Accept": "*/*"}

    async def get_puuid_and_region(
        self, player_name: str, player_tag: str
    ) -> str | None:
        # URL cua Henrikdev
        url = self.base_url + f"/v1/account/{player_name}/{player_tag}?force=true"

        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return data["data"]["puuid"], data["data"]["region"]
            error_msg = f"HenrikAPI Error: {response.status_code} - {response.text}"
            print(error_msg)  # In ra terminal (phòng hờ)
            raise HTTPException(status_code=response.status_code, detail=error_msg)

    





