import pymongo
from basic_data.dataModel import userData

class dbWrite():
    def __init__(self, userID):
      self.userID = userID
    
    # class userData(BaseModel):
    #     userDiscordID: str
    #     userGlobalName: str
    #     userAvatar:str
    #     Provider:str=None
    #     userEmail: str
    #     language: str=None
    def storeUser(self, userData):
        dbWrite=[]