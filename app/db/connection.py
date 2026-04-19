
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv
import os
from urllib.parse import quote_plus

dotenv.load_dotenv()

db_password = quote_plus(os.getenv("DB_PASSWORD"))

uri = f"mongodb+srv://24u1009:{db_password}@stack-of-luv-times.mpxka4a.mongodb.net/?appName=stack-of-luv-times"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)