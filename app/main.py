from fastapi import FastAPI
from .api.V1.api import api_router

app = FastAPI(title="CoreCraft", docs_url="/")
app.include_router(api_router, prefix="/api/v1")
