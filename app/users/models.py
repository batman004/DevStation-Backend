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
    role: str = Field(...)
    following_count: Optional[int] 
    following: Optional[list]
    followers_count: Optional[int] 
    followers: Optional[list]
    posts_id: Optional[list]
    request_created: Optional[list]
    request_accepted: Optional[list]
    disabled: Optional[bool] = None

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
                "role": "Backend",
                "following_count": 3,
                "following":["57hjhj5hg","748jhjkh75h","fhdjhjhkjfh"],
                "followers_count": 1,
                "followers": ["4jhkjl34hk"],
                "posts_id":["83iyuhh34","3hjkjkl4k4","djfjkjklh44"],
                "request_created" :["h4554h34","kjk66l4k4"],
                "request_accepted" :["443s554h34","&&%66l4k4"],
                "disabled":False
            }
        }

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UpdateUserModel(BaseModel):

    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    gender: Optional[str]
    phone: Optional[str]

    class Config:
        schema_extra = {
            "example": {

                "first_name": "Johny",
                "last_name": "Doe",
                "username": "John1234",
                "email": "john@gmail.com",
                "password": "##@@##**",
                "gender": "Male",
                "phone": "1234567855",
                "role": "Backend"
            }
        }

