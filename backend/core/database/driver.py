from pymongo import MongoClient

from backend.core.database.constant import CONNECTION_URL

client = MongoClient(CONNECTION_URL)
database = client.get_database()



