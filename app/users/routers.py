from fastapi import APIRouter, Body, HTTPException, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, oauth2
from .models import User, Token, TokenData, Login
from .hashing import Hash
from .jwt_token import create_access_token, verify_token
from .oauth import get_current_active_user
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

#router object for handling api routes
router = APIRouter()

@router.get("/",response_model=TokenData,response_description="Get token data of current user")
async def home(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
    user_token = verify_token(token,credentials_exception)
    print(user_token)
    return {"token":user_token}


# get user data {user_id},{username} -> user profile page
@router.get("/me",response_model=User, response_description="Get details of current active user")
async def read_root(current_user:User = Depends(get_current_active_user)):
	return current_user

# get all users
@router.get("/users", response_description="List all users")
async def list_users(request: Request):
    users = []
    for doc in await request.app.mongodb["users"].find().to_list(length=100):
        users.append(doc)
    return users

#login
@router.post("/login",response_model=Token, response_description="Login into app")
async def login(request:Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await request.app.mongodb["users"].find_one({"username":form_data.username})
    print(form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with username {form_data.username}')
    if not Hash.verify(user["password"],form_data.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')
    user["disabled"]=False
    access_token = create_access_token(data={"user": form_data.username })
    return {"access_token": access_token, "token_type": "bearer"}


#logout 
@router.post("/me/logout", response_description="Logout of the app")
async def logout(request:Request,current_user:User = Depends(get_current_active_user)):
    user = await request.app.mongodb["users"].find_one({"username":current_user.username})
    user["disabled"]=True
    return{"message":f"user{current_user.username} logged out"}

#signup
@router.post("/signup", response_description="Signup for a new user")
async def create_user(request: Request, user: User = Body(...)):
    user = jsonable_encoder(user)
    user["following"] = []
    user["posts_id"] = []
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
@router.post("/me/follow/{username_to_follow}",response_description="Follow a user")
async def follow_user(username_to_follow: str, request: Request, current_user:User = Depends(get_current_active_user)):
    user_to_follow = await request.app.mongodb["users"].find_one(
        {"username": username_to_follow}
    )
    user = await request.app.mongodb["users"].find_one(
        {"username": current_user}
    )
    request.app.mongodb["users"].update_one({"username":current_user.username}, {'$push': {'following': user_to_follow["_id"]}})
    request.app.mongodb["users"].update_one({"username":username_to_follow}, {'$push': {'followers': user["_id"]}})

    #count of number of following for current user
    count = len(user["following"]) + 1
    myquery = { "username": current_user.username }
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
    user = await request.app.mongodb["users"].find_one({"username":current_user.username})
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
@router.post("/me/follow/{username_to_unfollow}}",response_description="unfollow a user")
async def unfollow_user(username_to_unfollow: str, request: Request, current_user:User = Depends(get_current_active_user)):
    user_to_unfollow = await request.app.mongodb["users"].find_one(
        {"username": username_to_unfollow}
    )
    user = await request.app.mongodb["users"].find_one(
        {"username": current_user}
    )
    request.app.mongodb["users"].update_one({"username":current_user.username}, {'$pull': {'following': user_to_unfollow["_id"]}})
    request.app.mongodb["users"].update_one({"username":username_to_unfollow}, {'$pull': {'followers': user["_id"]}})
    
    #count of number of following for current user
    count = len(user["following"]) -1
    myquery = { "username": current_user.username }
    newvalues = { "$set": { "following_count": count } }
    request.app.mongodb["users"].update_one(myquery, newvalues)

    #count of number of followers for user which was unfollowed
    count_u = len(user_to_unfollow["followers"]) -1
    myquery_u = { "username": username_to_unfollow }
    newvalues_u = { "$set": { "followers_count": count_u } }
    request.app.mongodb["users"].update_one(myquery_u, newvalues_u)

    if(not user_to_unfollow==0):
        raise HTTPException(status_code=404, detail=f"Username : {username_to_unfollow} not found")
    return{"unfollowed":username_to_unfollow}



# delete current user
@router.delete("/me/delete", response_description="Delete user account")
async def delete_user(request: Request, current_user:User = Depends(get_current_active_user)):

    user = await request.app.mongodb["users"].find_one({"_id": current_user.id})
    # update posts collection as well when post is deleted

    for pid in user["posts_id"]:
        delete_post = await request.app.mongodb["posts"].delete_one({"_id": pid})
        #print("deleted post: ",pid)

    # remove user    
    delete_user = await request.app.mongodb["users"].delete_one({"_id": user["_id"]})
    if delete_user.deleted_count == 1:
        return {"deleted user" :current_user.id }

    raise HTTPException(status_code=404, detail=f"User {current_user.id} not found")





