from fastapi import APIRouter, Body, HTTPException, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from .models import RequestModel, UpdateRequestModel

router = APIRouter()

# Create collaborative request

@router.post("/create",response_description="Create a collaborative request")
async def create_request(request: Request, req: RequestModel = Body(...)):

    req_body = jsonable_encoder(req)
    req_body["accepted"]=False
    new_req = await request.app.mongodb["requests"].insert_one(req_body)
    created_req = await request.app.mongodb["requests"].find_one(
        {"_id": new_req.inserted_id}
    )

    #Adding post id to users collection
    request.app.mongodb["users"].update_one({"_id":created_req['user_to_request']}, {'$push': {'request_created': new_req.inserted_id}})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_req)


# Requests created by a user

@router.get("/created/{id}", response_description="List all requests from a user")
async def list_requests_created(id: str, request: Request):
    requests = []
    for doc in await request.app.mongodb["requests"].find({"user_to_request": id}).to_list(length=100):
        requests.append(doc)
    if(len(requests)!=0):

        return requests

    raise HTTPException(status_code=404, detail=f"User ID : {id} not found")


# Accept a request

@router.put("/{id}/accept", response_description="accept a request")
async def update_request(id: str, request: Request, req: UpdateRequestModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    if len(req) >= 1:
        req["accepted"] = True
        update_result = await request.app.mongodb["requests"].update_one(
            {"_id": id}, {"$set": req}
        )

        if update_result.modified_count == 1:
            if (
                updated_request := await request.app.mongodb["requests"].find_one({"_id": id})
            ) is not None:
                return updated_request

        # adding accepted requests to users collection
        new_req = await request.app.mongodb["requests"].find_one(
        {"_id": id})
        
        request.app.mongodb["users"].update_one(
        {"_id":new_req['user_to_accept']}, 
        {'$push': {'request_accepted': new_req["_id"]}})

    if (
        existing_request := await request.app.mongodb["requests"].find_one({"_id": id})
    ) is not None:
        return existing_request

    raise HTTPException(status_code=404, detail=f"Request {id} not found")


# Requests accepted by a user

@router.get("/accepted/{id}", response_description="List all requests from a user")
async def list_requests_accepted(id: str, request: Request):
    requests = []
    for doc in await request.app.mongodb["requests"].find({"user_to_accept": id}).to_list(length=100):
        requests.append(doc)
    if(len(requests)!=0):

        return requests

    raise HTTPException(status_code=404, detail=f"User ID : {id} not found")

