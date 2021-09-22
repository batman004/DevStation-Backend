#MongoDB driver
import motor.motor_asyncio
from model import Post

client = motor.motor_asyncio.AsyncIOMotorClient("localhost:27017")

db = client.devstation_DB
collection = db.posts

async def fetch_all_posts():
    posts = []
    cursor = collection.find({})
    async for document in cursor:
        posts.append(Post(**document))
    return posts

async def create_post(post):
    document = post
    result = await collection.insert_one(document)
    return document

async def update_post(username, body):
    await collection.update_one({"username": username}, {"$set": {"body": body}})
    document = await collection.find_one({"username": username})
    return document


# edit : update db to handle multiple posts from a user
async def remove_post(username):
    await collection.delete_one({"username": username})
    return True