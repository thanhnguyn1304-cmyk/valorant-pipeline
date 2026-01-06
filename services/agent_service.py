import httpx
from backend.models.agent import Agent
from sqlmodel import Session, select

class AgentService:
    def __init__(self, db_session):
        self.url = "https://valorant-api.com/v1/agents"
        agents_to_add = ([])  # adding agents now from the url as we didnt find in db earlier
    @staticmethod
    async def fetch_and_update_agents(db : Session):
        statement = select(Agent)  # build the query, checking the table we created above
        agents_in_db = db.exec(statement).all()
        if agents_in_db:
            print("Data found in pantry. Returning fast")
            return agents_in_db
        else:
            print("Pantry empty. Going to grocery store (API)...")
            agents_to_add = []
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
                    response = await client.get(AgentService.url)
                    data = response.json()
                    for agent_json in data["data"]:
                        new_agent = Agent(
                            displayIcon=agent_json["displayIcon"],
                            displayName=agent_json["displayName"],
                            role=agent_json["role"]["displayName"],
                            description=agent_json["description"],
                        )
                        db.add(new_agent)
                        agents_to_add.append(new_agent)

                    # added
            db.commit()

            for agent in agents_to_add:
                db.refresh(agent)
            return agents_to_add