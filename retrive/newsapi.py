from fastapi import FastAPI
import requests
from basic_data import const, data_checks

class NewsAPI:
    def __init__(self, api_key, url):
        self.api_key = api_key
        self.url = url
        
    def payload(self):
        params = {}
        params["qInTitle"] = const.const.searchin
        params["sources"] = const.const.sources
        params["domains"] = const.const.domains
        params["excludeDomains"] = const.const.excludeDomains
        return params

    async def get_news(self, interests=None, from_param=None, to_param=None, language="en"):
        
        params =self.payload()
        
        if interests is not None:
            params["q"] = " OR ".join(interests)
        else:
            interests = ["AI", "Geopolitics", "Space", "Technology"]
            params["q"] = " OR ".join(interests)
        
        if from_param is not None:
            params["from"] = from_param
            
        if to_param is not None:
            params["to"] = to_param
            
        params["language"] = language
        
        header = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url=self.url, headers=header, params=params)
        return {"news": f"Fetching news for interests: {', '.join(interests)}", "news_f": response.json()}

