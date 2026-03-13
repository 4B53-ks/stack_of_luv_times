from fastapi import APIRouter, Header, HTTPException
from retrive.newsapi import NewsAPI
from typing import Annotated
import datetime as dt
import dotenv
import os

env = dotenv.load_dotenv()
everything_url = os.getenv("fetchEverythingUrl")
top_headlines_url = os.getenv("fetchTopHeadlinesUrl")
sources_url = os.getenv("fetchSourcesUrl")
api_key = os.getenv("api_key")

router = APIRouter(
    prefix="/retrive",
    tags=["retrive"]
)

NewsAPI = NewsAPI(api_key=api_key, EverythingUrl=everything_url, topHeadlinesUrl=top_headlines_url, sourcesUrl=sources_url)

@router.get("/get-all-news/",
            description="Fetch news and filter by date range, date format should be YYYY-MM-DD and date to be entered till a month past only",
            summary="Fetch news with optional date filtering")
async def read_items(interests: Annotated[str, Header()], 
                     from_param: Annotated[dt.date, Header()] = None, 
                     to_param: Annotated[dt.date, Header()] = None,
                     language: Annotated[str, Header()] = None,
                     sortby: Annotated[str, Header()] = None):    
    interests_list = interests.split(",") if interests else []
    news = await NewsAPI.get_news(interests=interests_list, from_param=from_param, to_param=to_param, language=language, sortby=sortby)
    return news

#top headlines API call
@router.get("/top-headlines/",
            description="Fetch top headlines with optional country and category filtering",
            summary="Fetch top headlines with optional country and category filtering")
async def read_top_headlines(interests: Annotated[str, Header()] = None, 
                             country: Annotated[str, Header()] = None, 
                             category: Annotated[str, Header()] = None):
    
    interests_list = interests.strip().split(",") if interests else []
    news = await NewsAPI.get_top_headlines(interests=interests_list, country=country, category=category)
    return news
