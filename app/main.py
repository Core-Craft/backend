from fastapi import FastAPI
from .api.V1.api import api_router

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
