from backend.core.config import project_config
from backend.core.database.config import mongo_url
import motor.motor_asyncio


class DatabaseClient:

    def __init__(self, name: str):
        self.__client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
        self.__database = self.__client.get_database(name)

    @property
    def database(self):
        return self.__database

    @property
    def client(self):
        return self.__client


database_client = None


def init_database_client():
    global database_client
    database_client = DatabaseClient(project_config['database']['database_name'])


def get_database():
    global database_client
    return database_client


