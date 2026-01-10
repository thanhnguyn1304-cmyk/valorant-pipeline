from backend.services.riot_client import RiotClient
from backend.models import User
from sqlmodel import Select, Session, select

class PlayerService:
    def __init__(self):
        self.riot_client = RiotClient()
    def get_player_info(self, player_name: str, player_tag: str, db : Session):
        puuid, region = self.riot_client.get_puuid_and_region(player_name, player_tag)
        existing = select(User).where(User.puuid == puuid)
        if existing:
            return puuid, region
        else:
            new_user = User(puuid = puuid, user_id = player_name, user_tag = player_tag, region = region)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return puuid, region

        