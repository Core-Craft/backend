from fastapi import APIRouter, Request, Response, status, Depends, HTTPException, Query

from app.models.user import User as UserModel
from app.schemas.user import BaseUser, UserIn, UserOut, UserSearch
from .utils import hash_password, verify_password
import os
from typing import List

user = APIRouter()


@user.get("/users/", response_model=list[UserOut])
async def get_users():
    """
    Retrieve a list of users.

    Returns a list of user data in the response.

    This endpoint fetches user data from a data source and returns it as a list
    of UserOut objects, which include user id, full name, and email.

    Returns:
        List[UserOut]: A list of user data.
    """
    
    user_instance = UserModel()
    user_data = user_instance.get_all()

    return user_data


# @user.post("/users/filter/", response_model=UserOut)
# async def filter_users(filter: dict):
#     """api covers below features
#     1. user search (single/multiple)
#     """
    
#     user_instance = UserModel()  # Create an instance of the User model
#     print(filter)
    
#     # try:
#     #     filter_dict = filter.model_dump(exclude_unset=True)
#     # except ValueError as e:
#     #         raise HTTPException(status_code=400, detail=f"Invalid filter parameter: {e}")

#     # print(filter_dict)
#     user_data = user_instance.get(filter=filter)
#     UserOut.model_validate(user_data, from_attributes=True)
#     print(user_data)
    
    # return user_data
    
    
@user.post("/user/register/")
async def register_user(user_data: UserIn):
    
    # before entering data to db user search needs to be done using phone_no
    # password hashing needs to be done

    
#     user = db.query(db_name=db_name, table_name=table_name, filter={"_id"})
#     if user:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT,
#                             detail='Account already exist')

    
    user_instance = UserModel()

    try:
        user_dict = user_data.model_dump(exclude_unset=False)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid user data: {e}")

    try:
        user_instance.save(data=user_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register user: {e}")

    return {
        "status": "success",
        "message": "User registration successful",
        "data": {
            "id": user_dict["id"],
            "full_name": user_dict["name"],
            "phone_no": user_dict["phone"],
            }
        }
