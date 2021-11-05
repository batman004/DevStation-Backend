from fastapi import APIRouter, Body, HTTPException, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from .models import User, Token, TokenData, Login
from .hashing import Hash
from .jwt_token import create_access_token
from .oauth import get_current_active_user

#router object for handling api routes
router = APIRouter()

# get user data {user_id},{username} -> user profile page
@router.get("/me",response_model=User, response_description="Get details of current active user")
async def read_root(current_user:User = Depends(get_current_active_user)):
	return current_user

# get all users
@router.get("/users", response_description="List all users")
async def list_posts(request: Request):
    users = []
    for doc in await request.app.mongodb["users"].find().to_list(length=100):
        users.append(doc)
    return users

#login
@router.post("/login",response_model=Token, response_description="Login into app")
async def login(request:Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await request.app.mongodb["users"].find_one({"username":form_data.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with username {form_data.username}')
    if not Hash.verify(user["password"],form_data.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')
    access_token = create_access_token(data={"user": user["username"] })
    return {"access_token": access_token, "token_type": "bearer"}

#signup
@router.post("/signup", response_description="Signup for a new user")
async def create_user(request: Request, user: User = Body(...)):
    user = jsonable_encoder(user)
    user["following"] = []
    user["posts_id"] = []
    user["followers"] = []
    user["followers_count"] = 0
    user["following_count"] = 0
    hashed_pass = Hash.bcrypt(user["password"])
    user["password"] = hashed_pass
    new_user = await request.app.mongodb["users"].insert_one(user)
    created_user = await request.app.mongodb["users"].find_one(
        {"_id": new_user.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)

# follow a user
@router.post("/me/follow/{username_to_follow}",response_description="Follow a user")
async def follow_user(username_to_follow: str, request: Request, current_user:User = Depends(get_current_active_user)):
    user_to_follow = await request.app.mongodb["users"].find_one(
        {"username": username_to_follow}
    )
    user = await request.app.mongodb["users"].find_one(
        {"username": current_user}
    )
    request.app.mongodb["users"].update_one({"username":current_user}, {'$push': {'following': user_to_follow["_id"]}})
    request.app.mongodb["users"].update_one({"username":username_to_follow}, {'$push': {'followers': user["_id"]}})

    #count of number of following for current user
    count = len(user["following"]) + 1
    myquery = { "username": current_user }
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
@router.get("/me/feed", response_description="List all posts from the users which current user follows")
async def user_feed(request: Request, current_user:User = Depends(get_current_active_user)):
    following = []
    posts=[]
    user = await request.app.mongodb["users"].find_one({"username":current_user})
    for obj in user["following"]:
        following.append(obj)
    if(len(following)!=0):

        for users in following:
            user_followed = await request.app.mongodb["users"].find_one({"_id":users})
            for posts_id in user_followed["posts_id"]:
                post = await request.app.mongodb["posts"].find_one({"_id":posts_id})
                posts.append(post)
        return posts

    raise HTTPException(status_code=404, detail=f"Follow users to see their posts !")



# unfollow a user
# @router.delete("/{username}follow/{username_to_follow}",response_description="Follow a user")
# async def follow_user(username: str, username_to_follow: str, request: Request):
#     user = await request.app.mongodb["users"].find_one(
#         {"username": username_to_follow}
#     )

#     request.app.mongodb["users"].update_one({"username":username}, {'$push': {'following': user["id"]}})




# delete account


