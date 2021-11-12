from fastapi import Depends,HTTPException, Request
from .jwt_token import verify_token
from .models import User
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTPException(status_code=404),
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    verified_user = verify_token(token,credentials_exception)
    return verified_user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user