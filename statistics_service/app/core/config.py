from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int
    DB_NAME: str
    DB_NAME: str
    DB_STATISTICS_COLLECTION: str

    @property
    def database_url(self):
        return f"mongodb://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/"\
               f"{self.DB_NAME}?authSource=admin"

    class Config:
        env_file = '.env'


@lru_cache()
def get_settings() -> Settings:
    return Settings()
