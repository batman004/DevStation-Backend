# Reference : 

'''
GET     /users/{user_id}                     Get a User by their ID
DELETE  /users/{user_id}                     Remove a user by their ID
POST    /users/{user_id}/posts               Create a post from this user
GET     /users/{user_id}/followers           Get a list of followers of a user
GET     /users/{user_id}/followers_count     Get the number of followers of a user
GET     /users/{user_id}/following           Get the list of users this user is following
GET     /users/{user_id}/following_count     Get the number of users this user follows
GET     /users/{user_id}/posts               Get the messages sent by a user
GET     /users/{user_id}/timeline            Get the timeline for this user
PUT     /users/{user_id}                     Create a new user
PUT     /users/{user_id}/following/{target}  Follow a user
DELETE  /users/{user_id}/following/{target}  Unfollow a user

'''
from fastapi import Request
from .models import Post


async def fetch_all_posts(request: Request):
    posts = []
    cursor = request.app.mongodb["posts"].find({})
    async for document in cursor:
        posts.append(Post(**document))
    return posts

async def create_post(post, request: Request):
    document = post
    result = await request.app.mongodb["posts"].insert_one(document)
    return document

async def update_post(username, Updated_body, request: Request):
    await request.app.mongodb["posts"].update_one({"username": username}, {"$set": {"body": Updated_body}})
    document = await request.app.mongodb["posts"].find_one({"username": username})
    return document


# edit : update db to handle multiple posts from a user
async def remove_post(username, request: Request):
    await request.app.mongodb["posts"].delete_one({"username": username})
    return True