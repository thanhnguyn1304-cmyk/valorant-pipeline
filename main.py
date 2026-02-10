import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel
from backend.core.config import settings
from backend.core.database import engine
from backend.api.v1.api import api_router
# Import models so SQLModel knows about them
from backend.models.match import Match, MatchParticipation
from backend.models.user import User

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Create all tables on startup
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

origins = [
    # "http://localhost:3000",  # This is your React app's address
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Which "origins" (websites) are allowed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


app.include_router(api_router, prefix=settings.API_V1_STR)

# Serve static assets (rank images, etc.)
assets_dir = os.path.join(os.path.dirname(__file__), "assets")
app.mount("/static", StaticFiles(directory=assets_dir), name="static")


@app.get("/health")
def health_status():
    return {"status": "ok", "app_name": settings.PROJECT_NAME}
