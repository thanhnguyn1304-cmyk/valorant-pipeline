import httpx
from backend.core.config import settings
from fastapi import HTTPException


class MatchService:
    def __init__(self):
        self.base_url = "https://api.henrikdev.xyz/valorant"
        self.headers = {"Authorization": settings.ACCESS_TOKEN, "Accept": "*/*"}
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(10.0))

    async def get_matches_by_region_and_puuid(self, region: str, puuid: str):
        url = self.base_url + f"/v3/by-puuid/matches/{region}/{puuid}?mode=competitive&size=5"
        async with self.client as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return data["data"]
            error_msg = f"HenrikAPI Error: {response.status_code} - {response.text}"
            print(error_msg)  # In ra terminal (phòng hờ)
            raise HTTPException(status_code=response.status_code, detail=error_msg)
