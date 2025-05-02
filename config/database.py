from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

_client = None  # Cache client connection

def get_db():
    global _client

    if _client is None:
        try:
            _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
            _client.admin.command('ping')  # Test connection
            print("MongoDB connected successfully")
        except ConnectionFailure as e:
            print("MongoDB connection failed:", e)
            return None  # Return None instead of crashing

    return _client["hospital_db"]
