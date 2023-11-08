from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.models.subscription import Subscription as SubscriptionModel
from app.models.user import User as UserModel
from app.schemas.subscription import SubscriptionIn, SubscriptionUpdate

from .utils import get_current_user

subscription = APIRouter()


@subscription.get("/user/subscription/{user_uuid}", response_model=SubscriptionIn)
async def get_user_subscription(user_uuid: int, token: str = Depends(get_current_user)):
    """
    Get user subscription data by user UUID.

    This endpoint retrieves subscription data based on the provided user UUID. The response includes all subscription information for the user.

    Args:
        user_uuid (int): The unique identifier (UUID) of the user for whom to retrieve subscription data.

    Returns:
        SubscriptionIn: The subscription data for the user.

    Raises:
        HTTPException(404): If the user's subscription data is not found.
        HTTPException(500): If there is an internal server error while retrieving the data.
    """

    try:
        subscription_instance = SubscriptionModel()
        subscription_data = subscription_instance.get(uuid=user_uuid)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve subscription data: {e}"
        )

    if subscription_data is None:
        raise HTTPException(status_code=404, detail="Subscription data not found")

    return subscription_data


@subscription.get("/user/subscriptions/", response_model=List[SubscriptionIn])
async def get_user_subscriptions(token: str = Depends(get_current_user)):
    """
    Get a list of user subscriptions.

    This endpoint retrieves a list of all user subscription data. The response includes subscription information for all users.

    Returns:
        List[SubscriptionIn]: A list of user subscription data.

    Raises:
        HTTPException(404): If no user subscriptions are found.
        HTTPException(500): If there is an internal server error while retrieving the data.
    """
    try:
        subscription_instance = SubscriptionModel()
        subscription_data = subscription_instance.get_all()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve user subscriptions: {e}"
        )

    if len(subscription_data) == 0:
        raise HTTPException(status_code=404, detail="No user subscriptions found")

    return subscription_data


@subscription.post("/user/subscription/")
async def create_user_subscriptions(subscription: SubscriptionIn, token: str = Depends(get_current_user)):
    """
    Endpoint for creating user subscriptions.

    This endpoint allows users to create subscriptions for a given user based on the provided subscription data.

    Args:
        subscription (SubscriptionIn): The subscription data provided by the user.

    Returns:
        dict: A response dictionary containing the status, message, and subscription data if successful.

    Raises:
        HTTPException: If any errors occur during the subscription creation process, HTTP exceptions are raised
        with the appropriate status code and error details.
    """
    subscription_instance = SubscriptionModel()

    try:
        sub_dict = subscription.model_dump(exclude_unset=False)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid subscription data: {e}")

    try:
        user_instance = UserModel()
        user_data = user_instance.get(uuid=sub_dict["user_uuid"])
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve user data: {e}"
        )

    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        user_subscription = subscription_instance.filter(
            filter={"user_uuid": sub_dict["user_uuid"]}
        )
        if len(user_subscription) > 0:
            raise HTTPException(
                status_code=400,
                detail="User with this user_uuid already has a subscription",
            )
        else:
            try:
                response = subscription_instance.save(data=sub_dict)
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to register user subscription: {e}",
                )
    if response.acknowledged:
        return {
            "status": "success",
            "message": "Subscription added successfully",
            "data": {
                "user_uuid": sub_dict["user_uuid"],
                "amount": sub_dict["subscription"][0]["amount"],
            },
        }
    else:
        return {"status": "failure", "message": "Failed to create the subscription"}


@subscription.patch("/user/subscription/")
async def update_user_subscriptions(subscription: SubscriptionUpdate, token: str = Depends(get_current_user)):
    """
    Update a user's subscription.

    This endpoint updates a user's subscription based on the provided criteria in the SubscriptionUpdate model. The response includes a message of success or failure.

    Args:
        subscription (SubscriptionUpdate): The SubscriptionUpdate model containing filter criteria and updated subscription data.

    Raises:
        HTTPException(404): If no subscriptions are found.
        HTTPException(500): If there is an internal server error while retrieving or updating the data.

    Returns:
        dict: A dictionary containing the status of the update operation and a message.
            - "status" (str): Either "success" or "failure" indicating the result of the update.
            - "message" (str): A message describing the result of the update operation.
    """
    subscription_instance = SubscriptionModel()

    try:
        sub_dict = subscription.model_dump(exclude_unset=True)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid subscription data: {e}")

    try:
        existing_sub_data = subscription_instance.get(uuid=sub_dict["user_uuid"])
        if existing_sub_data:
            try:
                existing_sub_data["subscription"].append(sub_dict["user_data"])
                data = {
                    "user_uuid": sub_dict["user_uuid"],
                    "user_data": {"subscription": existing_sub_data["subscription"]},
                }
                response = subscription_instance.update(data=data)
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Failed to update subscription: {e}"
                )

            if response.acknowledged:
                return {
                    "status": "success",
                    "message": "Subscription updated successfully",
                    "data": {"user_uuid": sub_dict["user_uuid"]},
                }
            else:
                return {"status": "failure", "message": "Subscription update failed"}
        else:
            data = {
                "user_uuid": sub_dict["user_uuid"],
                "subscription": [sub_dict["user_data"]],
            }
            return await create_user_subscriptions(subscription=SubscriptionIn(**data))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve user data: {e}"
        )
