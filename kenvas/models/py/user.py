from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise import Tortoise
import uuid

from kenvas.models.db.user import User as UserTable

# Tortoise.init_models(["kenvas.models.db.user", "kenvas.models.db.activity"], "models")
User = pydantic_model_creator(UserTable)


class UserId(BaseModel):
    id: uuid.UUID


class UserEmail(BaseModel):
    email: str


class UserRegister(UserEmail):
    name: str
    password: str
    is_admin: bool = False


class UserLogin(UserEmail):
    password: str


class UserToken(UserEmail):
    username: str
    access_token: str
    token_type: str = "bearer"
    
    
class UserPublic(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    is_admin: bool
    
    
class UserPrivate(UserPublic):
    password: str
    access_token: str
    token_type: str = "bearer"