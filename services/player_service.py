from backend.services.riot_client import RiotClient
from backend.models.user import User
from sqlmodel import select, Session

class PlayerService:
    def __init__(self):
        self.riot_client = RiotClient()
    async def get_player_info(self, player_name: str, player_tag: str, db : Session):

        
        puuid, region = await self.riot_client.get_puuid_and_region(player_name, player_tag)
        existing = select(User).where(User.puuid == puuid)
        existing = db.exec(existing).first()
        if existing:
            if existing.user_id == player_name and existing.user_tag == player_tag :
                return puuid, region
            else:
                existing.user_id = player_name
                existing.user_tag = player_tag
                return puuid, region
        else:
            new_user = User(puuid = puuid, user_id = player_name, user_tag = player_tag, region = region)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return puuid, region

        