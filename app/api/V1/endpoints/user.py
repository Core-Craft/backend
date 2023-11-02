from typing import List

from fastapi import APIRouter, HTTPException

from app.models.user import User as UserModel
from app.schemas.user import UserIn, UserOut, UserSearch, UserUpdate, UserLogin
from .utils import hash_password, verify_password

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
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve existing user data: {e}"
        )

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
            - "status" (str): "success" indicating a successful registration or "failure" if the registration failed.
            - "message" (str): A message confirming the success or failure of the registration operation.
            - "data" (dict, optional): A dictionary containing user information, including ID, full name, and phone number, if the registration is successful.

    Raises:
        HTTPException: If the provided user data is invalid or if a user with the same email already exists.
    """

    user_instance = UserModel()

    try:
        user_dict = user_data.model_dump(exclude_unset=False)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid user data: {e}")

    if user_dict["email"]:
        # Checking for an existing user with the same email
        exist_users_list = user_instance.filter(filter={"email": user_data.email})
        if len(exist_users_list) > 0:
            raise HTTPException(
                status_code=400, detail="User with this email already exists"
            )

    try:
        encrypted_pass = hash_password(user_dict["password"])
        user_dict["password"] = encrypted_pass
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


@user.post("/user/login")
async def login_user(user_data: UserLogin):
    """
    Log in an existing user.

    This endpoint allows an existing user to log in based on the provided user data in the UserLogin model.

    Args:
        user_data (UserLogin): The UserLogin model containing user login data, including email and password.

    Returns:
        dict: A dictionary containing the status of the login operation and a message.
            - "status" (str): "success" indicating a successful login or "failure" if the login failed.
            - "message" (str): A message confirming the success or failure of the login operation.
            - "data" (dict, optional): A dictionary containing user information, including ID, full name, and phone number, if the login is successful.

    Raises:
        HTTPException 400: If the provided user data is invalid.
        HTTPException 500: If there is an issue with retrieving existing user data.
        HTTPException 404: If no user with the provided user_uuid exists.
        HTTPException 401: If the provided password is incorrect.
    """
    user_instance = UserModel()

    try:
        user_dict = user_data.model_dump(exclude_unset=True)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid request data: {e}")

    try:
        user_data = user_instance.filter(filter={"user_uuid": user_dict["user_uuid"]})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve existing user data: {e}"
        )

    if user_data:
        if verify_password(user_dict["password"], user_data[0]["password"]):
            return {
                "status": "success",
                "message": "User login successful",
                "data": {
                    "id": user_data[0]["user_uuid"],
                    "full_name": user_data[0]["full_name"],
                    "phone_no": user_data[0]["phone_no"],
                },
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        raise HTTPException(status_code=404, detail="User not found")


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

    Raises:
        HTTPException: If any errors occur during the user update process, HTTP exceptions are raised with the appropriate status code and error details.

    """
    user_instance = UserModel()

    try:
        user_dict = data.model_dump(exclude_unset=True)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid user data: {e}")
    
    try:
        user_instance = UserModel()
        user_data = user_instance.get(uuid=user_dict["user_uuid"])
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve user data: {e}"
        )

    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")

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
