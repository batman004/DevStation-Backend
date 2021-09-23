from pydantic import BaseModel

# class defined for a user post. Need to add likes and comments
class Post(BaseModel):
    username: str
    body: str


class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    gender: str
    phone: str
    address: str
    following: int 
    followers: int 

class Request(BaseModel):
    request_type: str       # help in a bug, partner in project etc
    dev_role: str           # Type of dev required : frontend, backend, app etc
    active_id: str


# class UserFeed(BaseModel):


# class defined for likes

# class defines for comments

#class defined for requests 

# class defined for user data

