from fastapi import APIRouter, Body, HTTPException
from .models import Post
from .database import (
    fetch_all_posts,
    create_post,
    update_post,
    remove_post
)

router = APIRouter()

@router.get("/")
def read_root():
    return {"Welcome to the default page"}

@router.get("/api/posts")
async def get_posts():
    response = await fetch_all_posts()
    return response


@router.post("/api/post/")
async def post_todo(post:Post):
    response = await create_post(post.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")


@router.put("/api/post{username}",response_model=Post)
async def put_todo(username, body):
    response = await update_post(username, body)
    if response:
        return response
    raise HTTPException(404, f"There is no post belonging to user : {username}")
    

# Login 

#Signup

# Follow

# Unfollow

# Like

# Request