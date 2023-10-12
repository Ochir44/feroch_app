from fastapi import APIRouter
from webapps.auth import route_login
from webapps.posts import route_posts
from webapps.users import route_users


api_router = APIRouter()

"""Routers that will contain information about users, posts and login in webapp"""

api_router.include_router(route_posts.router, prefix="", tags=["post-webapp"])
api_router.include_router(route_users.router, prefix="", tags=["users-webapp"])
api_router.include_router(route_login.router, prefix="", tags=["auth-webapp"])
