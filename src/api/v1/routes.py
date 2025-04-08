from fastapi import APIRouter

from api.v1 import auth, users, videos


def get_v1_routers() -> APIRouter:
    router = APIRouter(prefix="/v1")
    router.include_router(auth.router, tags=["Auth"])
    router.include_router(users.router, tags=["Users"])
    router.include_router(videos.router, tags=["Video"])
    return router
