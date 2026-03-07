from fastapi import APIRouter, Header
from retrive.newsapi import NewsAPI
from typing import Annotated
import datetime as dt
import dotenv
import os

env = dotenv.load_dotenv()
url = os.getenv("fetch_url")
api_key = os.getenv("api_key")

router = APIRouter(
    prefix="/retrive",
    tags=["retrive"]
)

NewsAPI = NewsAPI(api_key=api_key, url=url)

@router.get("/items/",
            description="Fetch news and filter by date range, date format should be YYYY-MM-DD and date to be entered till a month past only",
            summary="Fetch news with optional date filtering")
async def read_items(interests: Annotated[str, Header()], 
                     from_param: Annotated[dt.date, Header()] = None, 
                     to_param: Annotated[dt.date, Header()] = None):
    interests_list = interests.split(",") if interests else []
    news = await NewsAPI.get_news(interests_list, from_param, to_param)
    return news