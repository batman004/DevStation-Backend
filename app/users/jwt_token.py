from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import dotenv_values
config = dotenv_values(".env") 

from .models import TokenData
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=config["ACCESS_TOKEN_EXPIRE_MINUTES"])
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config["SECRET_KEY"], algorithm=config["ALGORITHM"])
    return encoded_jwt
def verify_token(token:str,credentials_exception):
 try:
     payload = jwt.decode(token, config["SECRET_KEY"], algorithms=[config["ALGORITHM"]])
     username: str = payload.get("sub")
     if username is None:
         raise credentials_exception
     token_data = TokenData(username=username)
 except JWTError:
     raise credentials_exception