from typing import List

from fastapi import APIRouter, HTTPException

from app.models.user import User as UserModel
from app.schemas.user import UserIn, UserOut, UserSearch

user = APIRouter()


@user.get(
    "/user/{user_uuid}", response_model=UserIn, response_model_exclude={"password"}
)
async def get_user(user_uuid: int):
    """
    Get user data by user_uuid.

    Args:
        user_uuid (int): The ID of the user to retrieve.

    Returns:
        UserIn: The user data excluding the 'password' field.
    """

    user_instance = UserModel()
    user_data = user_instance.get(user_uuid=user_uuid)

    return user_data


@user.get("/users/", response_model=list[UserOut])
async def get_users():
    """
    Retrieve a list of users.

    Returns a list of user data in the response.

    This endpoint fetches user data from a data source and returns it as a list
    of UserOut objects, which include user user_uuid, full name, and email.

    Returns:
        List[UserOut]: A list of user data.
    """

    user_instance = UserModel()
    user_data = user_instance.get_all()

    return user_data


@user.post("/users/filter/", response_model=List[UserOut])
async def filter_users(filter: UserSearch):
    """
    Filter users based on the provided filter criteria.

    Args:
        filter (UserSearch): The filter criteria for user search.

    Returns:
        List[UserOut]: A list of user data matching the filter criteria.
    """

    user_instance = UserModel()  # Create an instance of the User model
    try:
        user_dict = filter.model_dump(exclude_unset=True)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid filter parameter: {e}")

    try:
        user_data = user_instance.filter(filter=user_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register user: {e}")

    return user_data


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
            "id": user_dict["user_uuid"],
            "full_name": user_dict["full_name"],
            "phone_no": user_dict["phone_no"],
        },
    }


# @user.patch("/user/update/")
# async def register_user(user_data: UserIn):
#     """
#     sample json

#     {
#         "filter": {"key": "val"},
#         "data": {"key": "val"}
#     }

#     """
