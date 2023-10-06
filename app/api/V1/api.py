from fastapi import APIRouter

from app.api.V1.endpoints.subscription import subscription
from app.api.V1.endpoints.user import user

api_router = APIRouter()
api_router.include_router(user, tags=["User"])
api_router.include_router(subscription, tags=["Subscription"])
