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
@router.post("/signup", response_description="Signup for a new user")
async def create_user(request: Request, user: User = Body(...)):
    user = jsonable_encoder(user)
    user["following"] = []
    user["posts_id"] = []
    user["followers"] = []
    user["followers_count"] = 0
    user["following_count"] = 0
    new_user = await request.app.mongodb["users"].insert_one(user)
    created_user = await request.app.mongodb["users"].find_one(
        {"_id": new_user.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)





# get user data {user_id},{username} -> user profile page
@router.get("/{username}", response_description="List all details about a user")
async def list_posts(username: str, request: Request):
    if (user_data := await request.app.mongodb["users"].find_one({"username": username})) is not None:
        return user_data

    raise HTTPException(status_code=404, detail=f"User: {username} not found")


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



# User feed : show posts from the users that the current user has followed :
@router.get("/{username}/feed", response_description="List all posts from the users which current user follows")
async def user_feed(username: str, request: Request):
    following = []
    posts=[]
    user = await request.app.mongodb["users"].find_one({"username":username})
    print(user)
    for obj in user["following"]:
        following.append(obj)
    print(following)
    if(len(following)!=0):

        for users in following:
            user_followed = await request.app.mongodb["users"].find_one({"_id":users})
            for posts_id in user_followed["posts_id"]:
                post = await request.app.mongodb["posts"].find_one({"_id":posts_id})
                posts.append(post)
        return posts

    raise HTTPException(status_code=404, detail=f"Follow users !")



# unfollow a user
# @router.delete("/{username}follow/{username_to_follow}",response_description="Follow a user")
# async def follow_user(username: str, username_to_follow: str, request: Request):
#     user = await request.app.mongodb["users"].find_one(
#         {"username": username_to_follow}
#     )

#     request.app.mongodb["users"].update_one({"username":username}, {'$push': {'following': user["id"]}})




# delete account


