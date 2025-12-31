from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    CONNECTION_STRING: str
    ACCESS_TOKEN: str
    PROJECT_NAME: str = "ValorTracker"
    API_V1_STR: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",  # Nếu trong .env có biến lạ thì bỏ qua, không lỗi
    )


settings = Settings()
