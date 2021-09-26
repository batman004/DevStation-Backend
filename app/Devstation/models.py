from pydantic import BaseModel, Field
import uuid
from typing import Optional

# class defined for a user post. Need to add likes and comments
class Post(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str
    body: str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "username": "Jack",
                "body": "Hi I'm Jack and this is my first post!",
            }
        }



class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    first_name: str
    last_name: str
    username: str
    password: str
    gender: str
    phone: str
    address: str
    following: int 
    followers: int

    class Config:
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "first_name": "John",
                "last_name": "Doe",
                "username": "John123",
                "password": "#!@3$.yu&^%#$j12",
                "gender": "Male",
                "phone": "1234567890",
                "address": "12H, John Street",
                "following":45,
                "followers": 1000
            }
        }


class Request(BaseModel):
    request_type: str       # help in a bug, partner in project etc
    dev_role: str           # Type of dev required : frontend, backend, app etc
    active_id: bool

    class Config:
        schema_extra = {
            "example": {
                "request_type": "Bug",
                "dev_role": "Backend engineer",
                "active_id": True

            }
        }


# class UserFeed(BaseModel):


# class defined for likes


# class defines for comments


#class defined for requests 

# class defined for user data

