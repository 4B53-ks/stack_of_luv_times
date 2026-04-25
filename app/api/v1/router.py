# app/api/v1/router.py

from fastapi import APIRouter
from api.v1.endpoints import authAPI, retrive, basic_data, db_test

api_router = APIRouter()

api_router.include_router(authAPI.router)
api_router.include_router(retrive.router)
api_router.include_router(basic_data.router)
api_router.include_router(db_test.router)