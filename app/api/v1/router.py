# app/api/v1/router.py

from fastapi import APIRouter
from api.v1.endpoints import authAPI, retrive, basic_data

api_router = APIRouter()

api_router.include_router(authAPI.router, prefix="/auth", tags=["Auth"])
api_router.include_router(retrive.router, prefix="/news", tags=["News"])
api_router.include_router(basic_data.router, prefix="/basic", tags=["Basic"])