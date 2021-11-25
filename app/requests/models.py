import uuid
from typing import Optional
from pydantic import BaseModel, Field


class RequestModel(BaseModel):

    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    user_to_request: str = Field(...)
    user_to_accept: Optional[str]
    type: str = Field(...)
    body: str = Field(...)
    accepted: Optional[bool] = None


    class Config:
        schema_extra = {
            "example": {

                "user_to_request": "1b5b2986-8fc0-4c85-89ea-1e74bfc24118",
                "type": "Backend",
                "body": "hey I need help with CORS error",
                "accepted": False,
            }
        }

class UpdateRequestModel(BaseModel):

    user_to_accept: str = Field(...)
    accepted: Optional[bool] = None

    class Config:
        schema_extra = {
            "example": {
                "user_to_request": "1b5b2986-8fc0-4c85-89ea-1e74bfc24118",
                "user_to_accept": "52c03834-f0fa-4762-90ca-23d4feabde35",
                "type": "Backend",
                "body": "hey I need help with CORS error",
                "accepted": True,
            }
        }