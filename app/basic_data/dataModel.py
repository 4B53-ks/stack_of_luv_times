from pydantic import BaseModel
class newsResponse(BaseModel):
    news: str
    news_f: dict
    
class userData(BaseModel):
    userDiscordID: str
    userGlobalName: str
    userAvatar:str
    Provider:str=None
    userEmail: str
    language: str=None