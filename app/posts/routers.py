import datetime
from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .models import PostModel, UpdatePostModel, Comment

#router object for handling api routes
router = APIRouter()

@router.post("/", response_description="Add new post")
async def create_post(request: Request, post: PostModel = Body(...)):
    post = jsonable_encoder(post)
    current_datetime = str(datetime.datetime.now().strftime("%c"))
    post["time_added"]=current_datetime
    post["comments"]=[]
    post["likes"]=0
    new_post = await request.app.mongodb["posts"].insert_one(post)
    created_post = await request.app.mongodb["posts"].find_one(
        {"_id": new_post.inserted_id}
    )

    #Adding post id to users collection
    request.app.mongodb["users"].update_one({"username":created_post['username']}, {'$push': {'posts_id': new_post.inserted_id}})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_post)


@router.get("/", response_description="List all posts")
async def list_all_posts(request: Request):
    posts = []
    for doc in await request.app.mongodb["posts"].find().to_list(length=100):
        posts.append(doc)
    return posts


@router.get("/user/{username}", response_description="List all posts from a user")
async def list_posts(username: str, request: Request):
    posts = []
    for doc in await request.app.mongodb["posts"].find({"username": username}).to_list(length=100):
        posts.append(doc)
    if(len(posts)!=0):

        return posts

    raise HTTPException(status_code=404, detail=f"Username : {username} not found")



@router.get("/tag/{tag}", response_description="List all posts based on a tag")
async def list_tags(tag: str, request: Request):
    posts=[]
    for doc in await request.app.mongodb["posts"].find({"tags": tag }).to_list(length=100):
        posts.append(doc)
    if(len(posts)!=0):
        return posts

    raise HTTPException(status_code=404, detail=f"Tag : {tag} not found")

 


@router.get("/{id}", response_description="Get a single post")
async def show_post(id: str, request: Request):
    if (post := await request.app.mongodb["posts"].find_one({"_id": id})) is not None:
        return post

    raise HTTPException(status_code=404, detail=f"Post {id} not found")




@router.put("/{id}", response_description="Update a post")
async def update_post(id: str, request: Request, post: UpdatePostModel = Body(...)):
    post = {k: v for k, v in post.dict().items() if v is not None}
    current_datetime = str(datetime.datetime.now().strftime("%c"))
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
    
    
@router.post("/{id}/like", response_description="Like a post")
async def like_post(request: Request, id: str):
    post_to_like = await request.app.mongodb["posts"].find_one({"_id": id})
    if (post_to_like) is not None:
        likes = int(post_to_like['likes'] + 1)
        request.app.mongodb["posts"].update_one({"_id":id}, {'$set': {'likes':likes }})
        updated_post = await request.app.mongodb["posts"].find_one({"_id": id})
        return updated_post

    raise HTTPException(status_code=404, detail=f"Post {id} not found")

    

@router.post("/{id}/comment", response_description="Comment on a post")
async def comment_post(id: str, request: Request, comment: Comment = Body(...)):
    comment = jsonable_encoder(comment)
    current_datetime = str(datetime.datetime.now().strftime("%c"))
    comment["time_added"]=current_datetime
    new_comment = await request.app.mongodb["comments"].insert_one(comment)
    created_comment = await request.app.mongodb["comments"].find_one(
        {"_id":new_comment.inserted_id}
    )
    request.app.mongodb["posts"].update_one({"_id":id}, 
    {'$push': {'comments': created_comment["_id"]}})
    request.app.mongodb["comments"].update_one({"_id":new_comment.inserted_id},
    {'$set': {"post_id":id}})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_comment)


@router.get("/{id}/comments", response_description="Get the comments for a post")
async def show_comments(id: str, request: Request):
    if (posts := await request.app.mongodb["posts"].find_one({"_id": id})) is not None:
        comments = posts["comments"]
        return comments

    raise HTTPException(status_code=404, detail=f"Post {id} not found")

@router.get("/{id}/comment/metadata",response_description="get the details of a comment")
async def show_comment_details(id: str, request: Request):
    if (Comment := await request.app.mongodb["comments"].find_one({"_id": id})) is not None:
        return Comment

    raise HTTPException(status_code=404, detail=f"Comment {id} not found")
