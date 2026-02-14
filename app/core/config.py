# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Management REST API"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    # JWT
    SECRET_KEY: str = "super-secret-key"  # TODO: 本番環境では環境変数で設定
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()



