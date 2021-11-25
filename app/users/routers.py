from fastapi import APIRouter, Body, HTTPException, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from .models import User, Login, UpdateUserModel
from .hashing import Hash

#router object for handling api routes
router = APIRouter()

# get user data {user_id},{username} -> user profile page
@router.get("/{username}/details", response_description="Show all details about a user")
async def list_user(username: str, request: Request):
    if (user_data := await request.app.mongodb["users"].find_one({"username": username})) is not None:
        return user_data
    raise HTTPException(status_code=404, detail=f"User: {username} not found")

# get all users
@router.get("/users", response_description="List all users")
async def list_all_users(request: Request):
    users = []
    for doc in await request.app.mongodb["users"].find().to_list(length=100):
        users.append(doc)
    return users

# get top 3 users
@router.get("/users/top3", response_description="List top three users")
async def list_all_users(request: Request):
    users = []
    count=0
    for doc in await request.app.mongodb["users"].find().to_list(length=100):
        if(count>2):
            break
        users.append(doc)
        count+=1
    return users

#login
@router.post("/login")
async def login(request: Request, user_to_login: Login = Body(...)):
    user = await request.app.mongodb["users"].find_one({"username":user_to_login.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with username: {user_to_login.username}')
    if not Hash.verify(user["password"],user_to_login.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')
    user["disabled"]=False
    await request.app.mongodb["users"].update_one(
    {"_id": user["_id"]}, {"$set": user}
    )
    return {"message": "login successful"}

#logout 
@router.post("/logout", response_description="Logout of the app")
async def logout(username: str, request: Request):
    user = await request.app.mongodb["users"].find_one({"username":username})
    user["disabled"]=True
    await request.app.mongodb["users"].update_one(
    {"_id": user["_id"]}, {"$set": user}
    )
    return{"message":f"user: {username} logged out"}


#signup
@router.post("/signup", response_description="Signup for a new user")
async def create_user(request: Request, user: User = Body(...)):
    user = jsonable_encoder(user)
    user["following"] = []
    user["posts_id"] = []
    user["requests_created"] = []
    user["requests_accepted"] = []
    user["followers"] = []
    user["followers_count"] = 0
    user["following_count"] = 0
    user["disabled"]=True
    hashed_pass = Hash.bcrypt(user["password"])
    user["password"] = hashed_pass
    new_user = await request.app.mongodb["users"].insert_one(user)
    created_user = await request.app.mongodb["users"].find_one(
        {"_id": new_user.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


# follow a user
@router.post("/{username}/follow/{username_to_follow}",response_description="Follow a user")
async def follow_user(username: str, username_to_follow: str, request: Request):
    user_to_follow = await request.app.mongodb["users"].find_one(
        {"username": username_to_follow}
    )
    user = await request.app.mongodb["users"].find_one(
        {"username": username}
    )
    request.app.mongodb["users"].update_one({"username":username}, {'$push': {'following': user_to_follow["_id"]}})
    request.app.mongodb["users"].update_one({"username":username_to_follow}, {'$push': {'followers': user["_id"]}})

    #count of number of following for current user
    count = len(user["following"]) + 1
    myquery = { "username": username }
    newvalues = { "$set": { "following_count": count } }
    request.app.mongodb["users"].update_one(myquery, newvalues)

    #count of number of followers for user which was followed
    count_u = len(user_to_follow["followers"]) + 1
    myquery_u = { "username": username_to_follow }
    newvalues_u = { "$set": { "followers_count": count_u } }
    request.app.mongodb["users"].update_one(myquery_u, newvalues_u)

    # request.app.mongodb["users"].update_one({"username":username},{'following_count' :count })
    if(len(user_to_follow)==0):
        raise HTTPException(status_code=404, detail=f"Username : {username_to_follow} not found")
    return {"message": f"{username_to_follow} followed"}


# User feed : show posts from the users that the current user has followed :
@router.get("/{username}/feed", response_description="List all posts from the users which current user follows")
async def user_feed(username: str, request: Request):
    following = []
    posts=[]
    user = await request.app.mongodb["users"].find_one({"username":username})
    for obj in user["following"]:
        following.append(obj)
    if(len(following)!=0):

        for users in following:
            user_followed = await request.app.mongodb["users"].find_one({"_id":users})
            for posts_id in user_followed["posts_id"]:
                post = await request.app.mongodb["posts"].find_one({"_id":posts_id})
                posts.append(post)
        return posts

    # raise HTTPException(status_code=404, detail=f"Follow users !")
    return {"error":"follow users"}


# unfollow a user
@router.post("/{username}/unfollow/{username_to_unfollow}}",response_description="unfollow a user")
async def unfollow_user(username: str, username_to_unfollow: str, request: Request):
    user_to_unfollow = await request.app.mongodb["users"].find_one(
        {"username": username_to_unfollow}
    )
    user = await request.app.mongodb["users"].find_one(
        {"username": username}
    )
    request.app.mongodb["users"].update_one({"username":username}, {'$pull': {'following': user_to_unfollow["_id"]}})
    request.app.mongodb["users"].update_one({"username":username_to_unfollow}, {'$pull': {'followers': user["_id"]}})
    
    #count of number of following for current user
    count = len(user["following"]) -1
    myquery = { "username": username }
    newvalues = { "$set": { "following_count": count } }
    request.app.mongodb["users"].update_one(myquery, newvalues)

    #count of number of followers for user which was unfollowed
    count_u = len(user_to_unfollow["followers"]) -1
    myquery_u = { "username": username_to_unfollow }
    newvalues_u = { "$set": { "followers_count": count_u } }
    request.app.mongodb["users"].update_one(myquery_u, newvalues_u)

    if(len(user_to_unfollow)==0):
        raise HTTPException(status_code=404, detail=f"Username : {username_to_unfollow} not found")
    return {"message": f"{user_to_unfollow} unfollowed"}



# delete user
@router.delete("/{id}/delete", response_description="Delete user account")
async def delete_user(request: Request, id:str):

    user = await request.app.mongodb["users"].find_one({"_id": id})
    # update posts collection as well when post is deleted

    for pid in user["posts_id"]:
        delete_post = await request.app.mongodb["posts"].delete_one({"_id": pid})
        print("deleted post: ",pid)

    # remove user    
    delete_user = await request.app.mongodb["users"].delete_one({"_id": user["_id"]})
    if delete_user.deleted_count == 1:
        return {"message" :f"deleted user id: {id}"}

    raise HTTPException(status_code=404, detail=f"User {id} not found")



# Current active users :
@router.get("/active", response_description="Show all active users")
async def active_users( request: Request):
    users = []
    for doc in await request.app.mongodb["users"].find().to_list(length=100):
        # check if user is disabled or not
        if(not doc["disabled"]):
            users.append(doc)
    return users


# Edit user profile
@router.put("/update/{id}", response_description="Update user profile")
async def update_user(id: str, request: Request, user: UpdateUserModel = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}
    if len(user) >= 1:
        
        hashed_pass = Hash.bcrypt(user["password"])
        user["password"] = hashed_pass
        update_result = await request.app.mongodb["users"].update_one(
            {"_id": id}, {"$set": user}
        )

        if update_result.modified_count == 1:
            if (
                updated_user := await request.app.mongodb["users"].find_one({"_id": id})
            ) is not None:
                return updated_user

    if (
        existing_user := await request.app.mongodb["users"].find_one({"_id": id})
    ) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"User ID: {id} not found")
