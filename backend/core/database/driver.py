from backend.core.database.config import mongo_url
import motor.motor_asyncio


client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
database = client.get_database()
