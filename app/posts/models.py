import uuid
import datetime
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class PostModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str = Field(...)
    body: str = Field(...)
    # time_added: datetime = Field(default_factory=datetime.now(), alias="time_added")
    time_added:Optional[str]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "username": "John",
                "body": "Hello this is John",
                "time_added":"2021-10-07 00:02:13.886088"
            }
        }


class UpdatePostModel(BaseModel):

    body: str = Field(...)
    time_added: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "body": "hey this is my updated post",
                "time_added":"2021-10-07 00:03:13.886088"
            }
        }
