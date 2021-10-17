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
    likes:Optional[int]
    comments:Optional[list]
    tags:Optional[list]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "username": "John",
                "body": "Hello this is John",
                "time_added":"2021-10-07 00:02:13.886088",
                "likes":10,
                "comments":["jrk6659gfk","fjkj56565"],
                "tags":["#newpost","#firstpost","#lovethis","#newintech"]
            }
        }


class UpdatePostModel(BaseModel):

    body: str = Field(...)
    time_added: Optional[str]
    tags: Optional[list]

    class Config:
        schema_extra = {
            "example": {
                "body": "hey this is my updated post",
                "time_added":"2021-10-07 00:03:13.886088"
            }
        }

class Comment(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str = Field(...)
    body: str = Field(...)
    time_added: Optional[str]
    post_id:Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "body": "hey this is my comment",
                "username" :"john",
                "time_added":"2021-10-07 00:03:13.886088",
                "post_id":"00010203-0405-0607-0809-0a0b0c0d0e0f"
            }
        }
