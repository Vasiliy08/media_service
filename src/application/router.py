from fastapi import APIRouter

from src.application.api import router

main_router = APIRouter()
main_router.include_router(router)
