import uuid
from typing import Optional

from pydantic import BaseModel, Field


class PostModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str = Field(...)
    body: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "username": "John",
                "body": "Hello this is John",
            }
        }


class UpdatePostModel(BaseModel):
    username: str = Field(...)
    body: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "john",
                "body": "hey this is my updated post",
            }
        }
