from fastapi import APIRouter
from basic_data.const import const

router = APIRouter(
    prefix="/basic_data", 
    tags=["basic_data"]
)

@router.post("/country/")
def set_country(country):
    return const.set_country(country)