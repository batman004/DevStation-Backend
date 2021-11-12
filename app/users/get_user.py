from fastapi import HTTPException
from dotenv import dotenv_values
config = dotenv_values('.env')
from pymongo import MongoClient

mongodb_uri = config['DB_URL']
client = MongoClient(mongodb_uri, int(config['PORT']))
db = client[config['DB_NAME']]

def get_user(username: str):
    if (user_data := db["users"].find_one({"username": username})) is not None:
        return user_data
    raise HTTPException(status_code=404, detail=f"User: {username} not found")