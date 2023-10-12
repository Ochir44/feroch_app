from apis.version1 import route_login
from apis.version1 import route_posts
from apis.version1 import route_users
from fastapi import APIRouter


api_router = APIRouter()

"""Routers that will contain information about users, posts and login."""

api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(route_login.router, prefix="/login", tags=["login"])
