from pydantic import BaseSettings
import os
from decouple import config

class CommonSettings(BaseSettings):
    APP_NAME: str = "DevStation"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: config('MONGODB_URL')
    DB_NAME: config('DB_NAME')


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()