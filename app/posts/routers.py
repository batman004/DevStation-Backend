import datetime
from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .models import PostModel, UpdatePostModel

#router object for handling api routes
router = APIRouter()
current_datetime = str(datetime.datetime.now().strftime("%c"))

@router.post("/", response_description="Add new post")
async def create_post(request: Request, post: PostModel = Body(...)):
    post = jsonable_encoder(post)
    post["time_added"]=current_datetime
    new_post = await request.app.mongodb["posts"].insert_one(post)
    created_post = await request.app.mongodb["posts"].find_one(
        {"_id": new_post.inserted_id}
    )

    #Adding post id to users collection
    request.app.mongodb["users"].update_one({"username":created_post['username']}, {'$push': {'posts_id': new_post.inserted_id}})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_post)


@router.get("/", response_description="List all posts")
async def list_posts(request: Request):
    posts = []
    for doc in await request.app.mongodb["posts"].find().to_list(length=100):
        posts.append(doc)
    return posts


@router.get("/{username}", response_description="List all posts from a user")
async def list_posts(username: str, request: Request):
    posts = []
    for doc in await request.app.mongodb["posts"].find({"username": username}).to_list(length=100):
        posts.append(doc)
    if(len(posts)!=0):

        return posts

    raise HTTPException(status_code=404, detail=f"Username : {username} not found")



@router.get("/{id}", response_description="Get a single post")
async def show_post(id: str, request: Request):
    if (post := await request.app.mongodb["posts"].find_one({"_id": id})) is not None:
        return post

    raise HTTPException(status_code=404, detail=f"Post {id} not found")


@router.put("/{id}", response_description="Update a post")
async def update_post(id: str, request: Request, post: UpdatePostModel = Body(...)):
    post = {k: v for k, v in post.dict().items() if v is not None}

    if len(post) >= 1:
        post["time_added"]=current_datetime
        update_result = await request.app.mongodb["posts"].update_one(
            {"_id": id}, {"$set": post}
        )

        if update_result.modified_count == 1:
            if (
                updated_post := await request.app.mongodb["posts"].find_one({"_id": id})
            ) is not None:
                return updated_post

    if (
        existing_post := await request.app.mongodb["posts"].find_one({"_id": id})
    ) is not None:
        return existing_post

    raise HTTPException(status_code=404, detail=f"Post {id} not found")


@router.delete("/{id}", response_description="Delete Post")
async def delete_Post(id: str, request: Request):

    post = await request.app.mongodb["posts"].find_one({"_id": id})
    # update user collection as well when post is deleted
    request.app.mongodb["users"].update_one({"username":post['username']}, {'$pull': {'posts_id': post['_id']}})
    delete_result = await request.app.mongodb["posts"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Post {id} not found")

