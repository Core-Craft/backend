from typing import List

from fastapi import APIRouter, HTTPException

from app.models.user import User as UserModel
from app.schemas.user import UserIn, UserOut, UserSearch, UserUpdate
from .utils import hash_password

user = APIRouter()


@user.get(
    "/user/{user_uuid}", response_model=UserIn, response_model_exclude={"password"}
)
async def get_user(user_uuid: int):
    """
    Get user data by user UUID.

    This endpoint retrieves user data based on the provided user UUID. The response includes all user information except the 'password' field.

    Args:
        user_uuid (int): The unique identifier (UUID) of the user to retrieve.

    Returns:
        UserIn: The user data excluding the 'password' field.
    """

    try:
        user_instance = UserModel()
        user_data = user_instance.get(uuid=user_uuid)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve user data: {e}"
        )

    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")

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

    try:
        user_instance = UserModel()
        user_data = user_instance.get_all()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve user data: {e}"
        )

    if len(user_data) == 0:
        raise HTTPException(status_code=404, detail="No users found")

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
    """
    Register a new user.

    This endpoint allows registering a new user based on the provided user data in the UserIn model.

    Args:
        user_data (UserIn): The UserIn model containing user registration data.

    Returns:
        dict: A dictionary containing the status of the registration operation and a message.
            - "status": "success" indicating a successful registration.
            - "message": A message confirming the success of the registration operation.
            - "data": A dictionary containing user information including ID, full name, and phone number.
    """

    user_instance = UserModel()

    try:
        user_dict = user_data.model_dump(exclude_unset=False)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid user data: {e}")

    # checking existing user with email
    exist_users_list = user_instance.filter(
                filter={'email': user_data.email})
    if len(exist_users_list) > 0:
        raise HTTPException(status_code=400,
                            detail="User with this email already exists")

    try:
        # saving hashed password in db
        user_pass = user_dict['password']
        encypted_pass = hash_password(user_pass)
        user_dict['password'] = encypted_pass
        response = user_instance.save(data=user_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register user: {e}")

    if response.acknowledged:
        return {
            "status": "success",
            "message": "User registration successful",
            "data": {
                "id": user_dict["user_uuid"],
                "full_name": user_dict["full_name"],
                "phone_no": user_dict["phone_no"],
            },
        }
    else:
        return {"status": "failure", "message": "User registration failed"}


@user.patch("/user/update/")
async def update_user(data: UserUpdate):
    """
    Update user information.

    This endpoint allows updating user information based on the provided criteria in the UserUpdate model.

    Args:
        data (UserUpdate): The UserUpdate model containing filter criteria and updated user data.

    Returns:
        dict: A dictionary containing the status of the update operation and a message.
            - "status": Either "success" or "failure" indicating the result of the update.
            - "message": A message describing the result of the update operation.

    """
    user_instance = UserModel()

    try:
        user_dict = data.model_dump(exclude_unset=True)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid user data: {e}")

    try:
        response = user_instance.update(data=user_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {e}")

    if response.acknowledged:
        return {"status": "success", "message": "User update successful"}
    else:
        return {"status": "failure", "message": "User update failed"}


@user.delete("/user/delete/{user_uuid}")
async def delete_user(user_uuid: int):
    """
    Delete a user.

    This endpoint allows deleting a user based on the provided user UUID.

    Args:
        user_uuid (int): The unique identifier (UUID) of the user to be deleted.

    Returns:
        dict: A dictionary containing the status of the delete operation and a message.
            - "status": "success" indicating a successful deletion.
            - "message": A message confirming the success of the deletion operation.
    """

    user_instance = UserModel()

    try:
        user_instance = UserModel()
        user_data = user_instance.get(uuid=user_uuid)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve user data: {e}"
        )

    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        response = user_instance.delete(uuid=user_uuid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {e}")

    if response.acknowledged:
        return {"status": "success", "message": "User deletion successful"}
    else:
        return {"status": "failure", "message": "User deletion failed"}
