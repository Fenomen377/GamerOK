from pydantic_settings import BaseSettings
from pydantic import model_validator


class Settings(BaseSettings):
    DB_HOST:str
    DB_USER:str
    DB_PASS:str
    DB_NAME:str
    DB_PORT:int

    SECRET_KEY:str
    ALGORITHM:str
    DATABASE_URL: str | None = None

    @model_validator(mode='after')
    def get_database_url(cls, v):
        v.DATABASE_URL = f"postgresql+asyncpg://{v.DB_USER}:{v.DB_PASS}@{v.DB_HOST}:{v.DB_PORT}/{v.DB_NAME}"
        return v

    class Config:
        env_file = '.env'

settings = Settings()