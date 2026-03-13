from pydantic import BaseModel
class newsResponse(BaseModel):
    news: str
    news_f: dict