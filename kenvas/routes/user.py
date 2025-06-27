from fastapi import APIRouter, Depends, Query, Form
from fastapi.security import OAuth2PasswordRequestForm
import uuid
import jwt

from kenvas.models.py.user import User, UserId, UserToken, UserPublic
from kenvas.models.db.user import User as UserTable
from kenvas.utils import auth as U
from kenvas.exceptions import auth as E
from loguru import logger


router = APIRouter(prefix="", tags=["auth"])


@router.post("/register", dependencies=[Depends(U.get_current_active_superuser)], response_model=UserId)
async def create_user(
    name: str = Form(default="", description="Name of the user"),
    email: str = Form(default=..., description="Email of the user"),
    password: str = Form(default=..., description="Password of the user"),
    is_admin: bool = Form(default=False, description="Is the user an admin"),
):
    try:
        user = await UserTable.get(email=email).values()
    except:
        user = None

    if user:
        raise E.UserAlreadyExists()

    hashed_password = U.get_password_hash(password)
    user_id = uuid.uuid4()
    logger.info(user_id)
    await UserTable.create(
        id=user_id,
        name=name,
        email=email,
        password=hashed_password,
        is_admin=is_admin,
    )

    return UserId(id=user_id)


@router.post("/login", response_model=UserToken)
async def login_with_password(data: OAuth2PasswordRequestForm = Depends()):
    email, password = data.username, data.password
    try:
        user = await UserTable.get(email=email).values()
    except:
        user = None

    if not user:
        raise E.InvalidUsername()

    is_authenticated = U.authenticate_with_password(user["password"], password)
    if not is_authenticated:
        raise E.InvalidPassword()

    access_token = U.generate_access_token(data={"sub": email})

    return UserToken(username=email, email=email, access_token=access_token)


@router.get("/users/me", response_model=UserPublic)
async def login_with_token(user: UserTable = Depends(U.get_current_user)):
    
    if isinstance(user, E.InvalidToken):
        raise E.InvalidToken()
        
    print(user)
    
    # try:
    #     user = await UserTable.get(email=email).values()
    # except:
    #     user = None

    # if not user:
    #     raise E.InvalidUsername()

    return user


@router.get("/users", dependencies=[Depends(U.get_current_active_superuser)], response_model=list[UserPublic])
async def list_users():
    try:
        users = await UserTable.all()
        logger.info(users)
    except:
        users = None

    return users