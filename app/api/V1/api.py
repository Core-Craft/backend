from fastapi import APIRouter

from app.api.V1.endpoints.user import user

api_router = APIRouter()
api_router.include_router(user)
