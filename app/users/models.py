import uuid
from typing import Optional
from pydantic import BaseModel, Field, validator



class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    first_name: str = Field(...)
    last_name: str = Field(...)
    username: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    gender: str = Field(...)
    phone: str = Field(...)
    following: int = Field(...)
    followers: int = Field(...)
    posts_id: list

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v


    class Config:
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "first_name": "John",
                "last_name": "Doe",
                "username": "John123",
                "email": "john@gmail.com",
                "password": "##@@##**",
                "gender": "Male",
                "phone": "1234567890",
                "following":45,
                "followers": 1000,
                "posts_id":["8334","3h4k4","djfh44"]
            }
        }

