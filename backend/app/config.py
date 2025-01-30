from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}"
    secret_key: str

    class Config:
        env_file = ".env"

settings = Settings()