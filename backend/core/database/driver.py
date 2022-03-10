from pymongo import MongoClient

from backend.core.database.config import mongo_url

client = MongoClient(mongo_url)
database = client.get_database()




