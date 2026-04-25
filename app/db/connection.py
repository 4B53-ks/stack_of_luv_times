
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv
import os
from urllib.parse import quote_plus

dotenv.load_dotenv()

def check_active(active:str=None) -> bool:
    if "check" == active:
        pass
    else:
        raise ValueError(status_code=4853, error_msg="Random checks not to be given")
    
    db_password = quote_plus(os.getenv("DB_PASSWORD"))
    db_user = os.getenv("DB_USERNAME")
    db_cluster = os.getenv("CLUSTER_NAME")
    uri = f"mongodb+srv://{db_user}:{db_password}@{db_cluster}.mpxka4a.mongodb.net/?appName={db_cluster}"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return True
    except Exception as e:
        print(e)
        return False
    
def client_connect():
    db_password = quote_plus(os.getenv("DB_PASSWORD"))
    db_user = os.getenv("DB_USERNAME")
    db_cluster = os.getenv("CLUSTER_NAME")
    uri = f"mongodb+srv://{db_user}:{db_password}@{db_cluster}.mpxka4a.mongodb.net/?appName={db_cluster}"
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client
