# app/api/v1/api.py

from fastapi import APIRouter

from app.api.v1.endpoints import login, tasks, users

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(tasks.router, tags=["tasks"])



