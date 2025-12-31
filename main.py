from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

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


@app.get("/health")
def health_status():
    return {"status": "ok", "app_name": settings.PROJECT_NAME}
