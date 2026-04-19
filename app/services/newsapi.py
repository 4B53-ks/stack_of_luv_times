from fastapi import HTTPException
import requests
from basic_data import const
from basic_data import dataModel
import datetime as dt

class NewsAPI:
    def __init__(self, api_key, EverythingUrl, topHeadlinesUrl, sourcesUrl):
        self.api_key = api_key
        self.EverythingUrl = EverythingUrl
        self.topHeadlinesUrl = topHeadlinesUrl
        self.sourcesUrl = sourcesUrl

    def payload(self):
        params = {}
        params["sources"] = const.const.sources
        params["domains"] = const.const.domains
        params["excludeDomains"] = const.const.excludeDomains
        params["pageSize"] = const.const.pageSize
        params["page"] = const.const.page
        return params

    async def get_news(self, interests=None, from_param=None, to_param=None, language=None, sortby=None):
        
        params =self.payload()
        
        #interests
        if interests is None:
            raise HTTPException(status_code=400, detail="Interests header is required")
        if interests is not None:
            params["q"] = " + ".join(interests)
        else:
            interests = ["AI", "Geopolitics", "Space", "Technology"]
            params["q"] = " + ".join(interests)

        #sortby
        if sortby is not None:
            for item in sortby.split(","):
                if item.strip() not in const.const.sortBY:
                    raise HTTPException(status_code=400, detail=f"Invalid sortBy value: {item.strip()}")
            params["sortBy"] = sortby
        
        #date parameters
        for date_param in [from_param, to_param]:
            if date_param is not None:
                if not isinstance(date_param, dt.date):
                    raise HTTPException(status_code=400, detail="Date parameters must be in YYYY-MM-DD format")
                if date_param < (dt.date.today() - dt.timedelta(days=30)) or date_param > dt.date.today():
                    raise HTTPException(status_code=400, detail="Date parameters must be within the last month")
    
        if from_param is not None:
            params["from"] = from_param
            
        if to_param is not None:
            params["to"] = to_param
            
        #language
        if language is not None:
            if language not in const.const.languages:
                raise HTTPException(status_code=400, detail=f"Invalid language code: {language}")
        else:
            params["language"] = "en"
        
        #header
        header = {"Authorization": f"Bearer {self.api_key}"}
        
        #response
        response = requests.get(url=self.EverythingUrl, headers=header, params=params)
        
        #return
        return {
                "news": f"Fetching news for interests: {', '.join(interests)}", 
                "news_f": response.json()}
    
    async def get_top_headlines(self, interests=None, country=None, category=None) -> dataModel.newsResponse:
        
        params = self.payload()
        del params["domains"], params["excludeDomains"]
        
        #interests
        if interests is None:
            raise HTTPException(
                status_code=400, 
                detail="Interests header is required")
        if interests is not None:
            params["q"] = " + ".join(interests)
        else:
            interests = ["war"]


        #country
        if country is None:
            raise HTTPException(
                status_code=400, 
                detail="Country header is required")
        else:
            country = [item.strip() for item in country.split(",") if item.strip()]
            if len(country) != 1:
                raise HTTPException(
                    status_code=400,
                    detail=f"'country' must contain exactly 1 country code, got {len(country)}"
                )        
        if country is not None:
            if country not in const.const.COUNTRIES:
                raise HTTPException(status_code=400, detail=f"Invalid country code: {country}")
            params["country"] = country


        #category
        if category is not None:
            categories = [item.strip() for item in category.split(",") if category.strip()]
            category=[]
            for item in category:
                if item in const.const.category:
                    category.append(item)
                else:
                    raise HTTPException(status_code=400, detail=f"Invalid category: {item}")
                
            params["category"] = category
        else:
            params["category"]=const.const.category
        
        #header
        header = {"Authorization": f"Bearer {self.api_key}"}
        
        #response
        response = requests.get(url=self.topHeadlinesUrl, headers=header, params=params)
        
        
        #return
        return{
                "news": f"Fetching news for interests: {', '.join(interests)}", 
                "news_f": response.json()}
    

    

