import requests, uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel, Field, create_engine, Session, select, delete 
import json

import os
from dotenv import load_dotenv 
load_dotenv()

from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware




url = "https://valorant-api.com/v1/agents"
response = requests.get(url)
data = response.json()
print(response.status_code)


# 200 is ok, 404 = not found, 403/401 = forbidden/ unauthorized

# print(response.text) to see whats really in there sometimes 200 but the actual message was 'rate limit exceeded' that won't work

# print(data['data'][0]['displayName']) prints out Gekko

# 1. create database


# OLD, BAD CODE:
# database_connection_string = 'postgresql://postgres:thanh1304@localhost:5432/valorant_db'

# NEW, SECURE CODE:
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    # This is better than a confusing "password failed" error later.
    raise ValueError("One or more database environment variables are missing from .env")

# Build the string from the variables
# This code is now 100% flexible and has NO secrets.
database_connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"






engine = create_engine(database_connection_string, echo = True) 

class Agent(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key = True)
    displayName : str
    role : str
    description : str
    displayIcon: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    # create db
    SQLModel.metadata.create_all(engine)

    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",  # This is your React app's address
]

app.add_middleware( 
    CORSMiddleware,
    allow_origins=origins,  # Which "origins" (websites) are allowed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

#2. we do the updating part

@app.get("/agents")
def get_all_agents():
    
    #2.1 returning db

    with Session(engine) as session: #Session is the shopping cart, use session.add() and session.commit() to checkout
        statement = select(Agent) # build the query, checking the table we created above
        results = session.exec(statement) # run the query
        agents_in_db = results.all() #returning what have been found
        
        if agents_in_db :
            print('Data found in pantry. Returning fast')
            return agents_in_db
        
        #2.2 if db is empty, go take it from website
        
        else:
            print('Pantry empty. Going to grocery store (API)...')
            


            response = requests.get(url)
            data = response.json()
            
            #for agent_json in data['data']:

            # first agent checkng raw json using print(json.dumps(...))

            # --- Our New Debug Code ---
            #first_agent_data = data['data'][0] 
            
            #print("--- First Agent Data ---")
            #print(json.dumps(first_agent_data, indent=4))
            
            #print("------------------------")

            
            agents_to_add = [] #adding agents now from the url as we didnt find in db earlier

            for agent_json in data['data']:
                new_agent = Agent(
                displayIcon=agent_json['displayIcon'],
                displayName=agent_json['displayName'],
                role=agent_json['role']['displayName'],
                description=agent_json['description'],
                )
                session.add(new_agent)
                agents_to_add.append(new_agent)
            
            session.commit()
            
            for agent in agents_to_add:
                session.refresh(agent)
            return agents_to_add

#done with the update part in CRUD, now we go to the delete part

@app.post("/refresh-agents")
def refresh_agents_cache():
    with Session(engine) as session:
        statement = delete(Agent) 
        #deleting everything, can add where(Agent.displayName == "Jett")), delete(Agent)
        session.exec(statement)
        session.commit()
        return 'Cache is cleared. Pantry is now empty'