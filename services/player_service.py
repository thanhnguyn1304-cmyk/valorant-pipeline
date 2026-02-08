from backend.services.riot_client import RiotClient
from backend.models.user import User
from sqlmodel import select, Session

class PlayerService:
    def __init__(self):
        self.riot_client = RiotClient()
    async def get_player_info(self, player_name: str, player_tag: str, db : Session):
        # 1. Check DB first (Optimization)
        statement = select(User).where(User.user_id == player_name, User.user_tag == player_tag)
        existing_user = db.exec(statement).first()
        
        if existing_user:
            return existing_user.puuid, existing_user.region

        # 2. Only if not in DB, call API
        puuid, region = await self.riot_client.get_puuid_and_region(player_name, player_tag)
        
        # 3. Check if PUUID exists (maybe name changed?)
        existing_puuid = select(User).where(User.puuid == puuid)
        existing_puuid_user = db.exec(existing_puuid).first()

        if existing_puuid_user:
            # Update name/tag if changed
            if existing_puuid_user.user_id != player_name or existing_puuid_user.user_tag != player_tag:
                existing_puuid_user.user_id = player_name
                existing_puuid_user.user_tag = player_tag
                db.add(existing_puuid_user)
                db.commit()
                db.refresh(existing_puuid_user)
            return puuid, region
        else:
            # Create new user
            new_user = User(puuid=puuid, user_id=player_name, user_tag=player_tag, region=region)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return puuid, region

        