from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .models import User

#router object for handling api routes
router = APIRouter()

# get all users
@router.get("/", response_description="List all users")
async def list_posts(request: Request):
    users = []
    for doc in await request.app.mongodb["users"].find().to_list(length=100):
        users.append(doc)
    return users




#login





#signup





# get user data {user_id},{username} -> user feed

# follow a user

# unfollow a user

# delete account

# list user posts

