# DevStation-Backend

### Tech stack
- FastAPI (Python)
- MongoDB

### Database Schema

#### Post
```
    id: str 
    username: str 
    body: str 
    time_added: str
    likes:int
    comments:list
    tags:list
    
                "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "username": "John",
                "body": "Hello this is John",
                "time_added":"2021-10-07 00:02:13.886088",
                "likes":10,
                "comments":["jrk6659gfk","fjkj56565"],
                "tags":["#newpost","#firstpost","#lovethis","#newintech"]
                }
```

#### User
```
    id: str
    first_name: str 
    last_name: str 
    username: str
    email: str
    password: str 
    gender: str 
    phone: str 
    following_count: int
    following: list
    followers_count: int
    followers: list
    posts_id: list
    disabled: bool
    

            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "first_name": "John",
                "last_name": "Doe",
                "username": "John123",
                "email": "john@gmail.com",
                "password": "##@@##**",
                "gender": "Male",
                "phone": "1234567890",
                "following_count": 3,
                "following":["57hjhj5hg","748jhjkh75h","fhdjhjhkjfh"],
                "followers_count": 1,
                "followers": ["4jhkjl34hk"],
                "posts_id":["83iyuhh34","3hjkjkl4k4","djfjkjklh44"],
                "disabled":False
            }
```
 
### API Routes

## V 1.0

#### Post
Routes | HTTP | Description
--- | --- | ---
**/post/** | `GET` | Get all posts
**/post/{id}** | `GET` | Get Single post
**/post/** | `POST` | Create a post
**/post/{id}** | `DELETE` | Delete a post
**/post/{id}** | `PUT` | Update data of a post
**/post/users/{username}** | `GET` | Get posts from a user
**/post/tag/{tag}** | `GET` | Get posts with a requested tag
**/post/{id}/like** | `POST` | Like a post
**/post/{id}/comment** | `POST` | Comment on a post
**/post/{id}/comments** | `GET` | Show comments on a post
**/post/{id}/comment/metadata** | `GET` | Show data about comment on a post


#### User
Routes | HTTP | Description
--- | --- | ---
**/user/active** | `GET` | Get all active users
**/user/{username}/details** | `GET` | Get Single user
**/user/** | `POST` | Create a user
**/user/login** | `POST` | Login a user
**/user/logout** | `POST` | Logout a user
**/user/{username}/follow/{username_to_follow}** | `POST` | Follow a user
**/user/{username}/unfollow/{username_to_unfollow}** | `POST` | Unfollow a user
**/user/{username}/feed** | `GET` | Get feed of logged in user
**/user/{id}/delete** | `DELETE` | Delete a user


## V 1.1

- Added Authentication using JWT token


**Login**
----
Logs in a user and returns JWT token with a validity of 30 minutes
* **URL**

    /user/token

* **Method:**

    `POST`
  

* **Data Params**

    `username=str`
    
   `password=str`
    
   
* **Success Response:**
  
  * **Code:** 200 <br />
  
    **Content:** 
    
   ```
   {
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiam9objEyMyIsImV4cCI6MTYzNzY5NDYzNH0.7jFLeyqpMDi4bHyj9zcrG1kQ0N-2-Ij7dijdWt4IHpU",
  "token_type": "bearer"
    }
    ```
    
 
* **Error Response:**

* **Code:** 404 NOT FOUND <br />

    **Content:** `{"detail": "No user found with username <username>" }`


* **Sample Call:**

```
curl -X 'POST' \
  'http://0.0.0.0:8000/user/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=john123&password=<password>&scope=&client_id=&client_secret='
```

### Authenticated routes

Routes | HTTP | Description
--- | --- | ---
**/user/** | `GET` | Get token of logged in user
**/user/me** | `GET` | Get details of current user
**/user/me/feed** | `GET` | Get feed of current user
**/user/** | `POST` | Create a user
**/user/login** | `POST` | Login a user
**/user/me/logout** | `POST` | Logout current user
**/user/me/follow/{username_to_follow}** | `POST` | Follow a user
**/user/me/unfollow/{username_to_unfollow}** | `POST` | Unfollow a user
**/user/me/delete** | `DELETE` | Delete current user
**/post/** | `POST` | Create a post
**/post/{id}** | `DELETE` | Delete a post
**/post/{id}** | `PUT` | Update data of a post
**/post/{id}/like** | `POST` | Like a post
**/post/{id}/comment** | `POST` | Comment on a post


* **Sample request for post creation after authentication**

```
curl -X 'POST' \
  'http://0.0.0.0:8000/post/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer {JWT_TOKEN}“  \
  -d '{
  "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
  "username": "John",
  "body": "Hello this is John",
  "time_added": "2021-10-07 00:02:13.886088",
  "likes": 10,
  "comments": [
    "jrk6659gfk",
    "fjkj56565"
  ],
  "tags": [
    "#newpost",
    "#firstpost",
    "#lovethis",
    "#newintech"
  ]
}'
```


## Status Codes

DevStation-API returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |


### Installation guide
```
git clone https://github.com/batman004/DevStation-Backend.git
cd DevStation-Backend
vi .env
<fill in credentials>
    DB_URL=
    DB_NAME=
    PORT= 
    PROD=
    JWT_SECRET_KEY=
    ALGORITHM=
    ACCESS_TOKEN_EXPIRE_MINUTES=
python main.py
```


## Link to frontend repo 

 - https://github.com/AviroopNandy/dev-station

### Currently under Development 🛠 ⚙️

![Devstation Homepage](https://user-images.githubusercontent.com/58564635/138453291-83c4ed3b-975e-41ef-8bb3-cb66dcffe15d.gif)

