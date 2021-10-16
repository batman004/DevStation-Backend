from pydantic import BaseSettings
from dotenv import dotenv_values
import os

config = dotenv_values(".env") 
prod = False

class CommonSettings(BaseSettings):
    APP_NAME: str = "DevStation"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000

if prod ==True:
    class DatabaseSettings(BaseSettings):
        DB_URL: str = os.environ['DB_URL']
        DB_NAME: str = os.environ['DB_NAME'] 

else :
    class DatabaseSettings(BaseSettings):
        DB_URL: str = config['DB_URL']
        DB_NAME: str = config['DB_NAME'] 

class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()