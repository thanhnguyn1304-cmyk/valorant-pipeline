import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    CONNECTION_STRING: str
    ACCESS_TOKEN: str
    GEMINI_API_KEY: str = ""
    PROJECT_NAME: str = "ValorTracker"
    API_V1_STR: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_ignore_empty=True,
        extra="ignore",
    )


settings = Settings()
