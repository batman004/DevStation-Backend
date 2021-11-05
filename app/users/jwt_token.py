from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import dotenv_values
config = dotenv_values('.env')
from .models import TokenData

TD = int(config['ACCESS_TOKEN_EXPIRE_MINUTES'])

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TD)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config['JWT_SECRET_KEY'], algorithm=config['ALGORITHM'])
    return encoded_jwt
def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token, config['JWT_SECRET_KEY'], algorithm=config['ALGORITHM'])
        username: str = payload.get("user")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        return token_data.username
    except JWTError:
        raise credentials_exception
