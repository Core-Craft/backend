from typing import List

from fastapi import APIRouter, HTTPException

# from app.models.user import User as UserModel
from app.schemas.subscription import SubscriptionIn

subscription = APIRouter()


@subscription.get("/subscriptions/", response_model=SubscriptionIn)
async def get_subscriptions():
    pass
