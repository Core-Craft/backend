from typing import List

from fastapi import APIRouter, HTTPException

from app.models.subscription import Subscription as SubscriptionModel
from app.schemas.subscription import SubscriptionIn
from app.models.user import User as UserModel

subscription = APIRouter()


@subscription.get("/user/subscription/{user_uuid}", response_model=SubscriptionIn)
async def get_user_subscription(user_uuid: int):
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
async def get_user_subscriptions():
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


@subscription.post("/user/subscription/", response_model=SubscriptionIn)
async def create_user_subscriptions(subscription: SubscriptionIn):
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
        sub_dict = subscription.model_dump(exclude_unset=False)
        if sub_dict["user_uuid"]:
            user_instance = UserModel()
            user_data = user_instance.get(uuid=sub_dict["user_uuid"])
            if user_data is None:
                raise Exception("No user with this UUID")

            user_subs = subscription_instance.filter(filter={"user_uuid":sub_dict["user_uuid"]})
            if len(user_subs) > 0:
                raise HTTPException(status_code=400, detail="User with this \
email already exists")

        subscription_data = subscription_instance.save(data=sub_dict)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve user subscriptions; Error:  {e}"
        )

    if subscription_data.acknowledged:
        return {
            "status": "success",
            "message": "Subscription for user created successfully",
            "data": {
                "id": sub_dict["user_uuid"],
                "amount": sub_dict["subscription"][0]["amount"],
            },
         }
    else:
        return {"status": "failure", "message": "Subscription Creation failed"}
