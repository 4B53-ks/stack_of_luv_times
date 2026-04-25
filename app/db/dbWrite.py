import pymongo
from basic_data.dataModel import userData
import os
import dotenv
from db.connection import client_connect

class dbWritesome():
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
        
def db_write(data, db_name:str=None, collection_name:str=None) -> str:
  client = client_connect()
  
  dotenv.load_dotenv()
  if None == db_name:
      db = client[os.getenv("DB_NAME")]
  else:
      db = client[db_name]
    
  if None == collection_name:
      collection = db[os.getenv("USER_COLLECTION")]
  else:
      collection = db[collection_name]
    
  response = collection.insert_one(data)
  return str(response)