from functools import lru_cache
from pydantic import BaseSettings
import sys


class Settings(BaseSettings):
    SECRET_KEY: str
    HASH_ALGORITHM: str
    TOKEN_EXPIRE_MINUTES: int
    AUTHENTICATION_HEADER_PREFIX: str
    DBMS: str
    DB_HOST: str
    DB_DRIVER: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int
    DB_NAME: str
    AWS_ACCESS_KEY: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET_NAME: str
    AWS_S3_REGION: str
    RB_HOST: str
    RB_PORT: int
    RB_QUEUE_NAME: str
    RB_USER: str
    RB_PASSWORD: str
    MAINTAINCE_MODE: bool

    @property
    def broker_url(self):
        return (
            f"amqp://{self.RB_USER}:{self.RB_PASSWORD}@{self.RB_HOST}:{self.RB_PORT}//"
        )

    @property
    def database_url(self) -> str:
        return f"{self.DBMS}+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def aws_s3_bucket_file_url(self) -> str:
        return (
            f"https://s3-{self.AWS_S3_REGION}.amazonaws.com/{self.AWS_S3_BUCKET_NAME}/"
        )

    class Config:
        if "pytest" in sys.modules:
            env_file = ".env.test"
        else:
            env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
