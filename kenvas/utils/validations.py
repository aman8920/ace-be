from tortoise import exceptions as TortoiseExceptions

from kenvas.exceptions import auth as AuthExceptions
from kenvas.models.db.user import User as UserTable
from kenvas.models.py.user import User
# from kenvas.logging.app import logger


async def validate_user_exists(email: str) -> User:
    """checks if the user exists in the database

    Args:
        email (str): email of the user

    Raises:
        AuthExceptions.InvalidUsername: username/email does not exist in the database

    Returns:
        User: user details
    """

    try:
        user = await UserTable.get(email=email)
        return user
    except TortoiseExceptions.DoesNotExist:
        raise AuthExceptions.InvalidUsername()


# async def validate_activity_exists(activity_id: str) -> Activity:
#     """checks if the given activity exists for the given user

#     Args:
#         user_id (str): uuid of the user
#         activity_id (str): uuid of the activity

#     Raises:
#         ActivityExceptions.ActivityDoesNotExist: activity does not exist for the given user

#     Returns:
#         Activity: activity details
#     """
#     try:
#         activity = await ActivityTable.get(id=activity_id)
#         return activity
#     except TortoiseExceptions.DoesNotExist as exc:
#         raise ActivityExceptions.ActivityDoesNotExist(exception=exc)
    

# async def validate_activity_user(user_id: str, activity_id: str) -> ActivityId:
#     """checks if the given activity exists for the given user

#     Args:
#         user_id (str): uuid of the user
#         activity_id (str): uuid of the activity

#     Raises:
#         ActivityExceptions.ActivityDoesNotExist: activity does not exist for the given user

#     Returns:
#         Activity: activity details
#     """
#     try:
#         activity_id = await ActivityUserTable.get(user_id=user_id, activity_id=activity_id)
#         return activity_id
#     except TortoiseExceptions.DoesNotExist as exc:
#         raise ActivityExceptions.ActivityDoesNotExist(exception=exc)