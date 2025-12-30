import httpx
from backend.core.config import settings


class RiotClient:
    def __init__(self):
        self.base_url = "https://api.henrikdev.xyz/valorant"
        self.access_token = settings.ACCESS_TOKEN
        self.headers = {"Authorization": self.access_token, "Accept": "*/*"}
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(10.0))

    async def get_puuid(self, player_name: str, player_tag: str) -> str | None:
        # URL cua Henrikdev
        url = self.base_url + "v1/account/{player_name}/{player_tag}"

        async with self.client as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return data["data"]["puuid"]
            else:
                print(f"Error fetching PUUID: {response.status_code} - {response.text}")
                return None
