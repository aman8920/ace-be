from datetime import datetime, timedelta, timezone
from os import getenv as env
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from loguru import logger
from fastapi import Depends, HTTPException, status
from kenvas.models.db.user import User as UserTable
from kenvas.exceptions import auth as E
from loguru import logger

# to get a string like this run:
# openssl rand -hex 32
# JWT_SECRET = env("JWT_SECRET")
# ALGORITHM = env("ALGORITHM")
JWT_SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(env("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=True)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_with_password(hashed_password: str, plain_password: str):
    is_authenticated = pwd_context.verify(plain_password, hashed_password)
    return is_authenticated


def generate_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    logger.info(to_encode)
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user = await UserTable.get(email=username)
        if username is None:
            return None
        return user
    except jwt.ExpiredSignatureError:
        raise E.InvalidToken()
    except Exception as e:
        return None
    
    
def get_current_active_superuser(current_user = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user