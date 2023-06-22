from functools import lru_cache

from pydantic import BaseSettings


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    db_url: str = "sqlite:///local.db"
