from fastapi import APIRouter

from src.auth.routes import auth_router
from src.users.routes import users_router
from src.ghibli.routes import ghibli_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(ghibli_router, prefix="/ghibli", tags=["ghibli"])