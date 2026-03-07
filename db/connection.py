
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
import dotenv
import os

dotenv.load_dotenv()
db_username = os.getenv("DB_USERNAME")
db_password = quote_plus(os.getenv("DB_PASSWORD"))
db_name = os.getenv("DB_NAME")
uri = f"mongodb+srv://{db_username}:{db_password}@stack-of-luv-times.mpxka4a.mongodb.net/{db_name}?appName=stack-of-luv-times"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)