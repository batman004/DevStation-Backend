from fastapi import Request, HTTPException

async def get_user(username: str, request: Request):
    if (user_data := await request.app.mongodb["users"].find_one({"username": username})) is not None:
        return user_data
    raise HTTPException(status_code=404, detail=f"User: {username} not found")