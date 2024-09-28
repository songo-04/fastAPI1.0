
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()


# Create a new client and connect to the server
client = MongoClient(os.getenv("uri_offline"), server_api=ServerApi('1'))
db=client.fastAPIDb
user_collection = db['users']
contact_collection = db['contacts']
task_collection = db['tasks']
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)