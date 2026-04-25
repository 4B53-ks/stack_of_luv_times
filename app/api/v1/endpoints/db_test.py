from fastapi import APIRouter
from db.dbWrite import db_write

router = APIRouter(
    prefix = '/db',
    tags=["db"]
)

@router.post('/test')
def db_test(data: dict[str, str]):
    if None == data:
        raise ValueError
    else:
        response = db_write(data=data)
        return response
        