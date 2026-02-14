# app/main.py

from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="JWT認証付きタスク管理API",
    version="1.0.0",
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Task Management API!"}

