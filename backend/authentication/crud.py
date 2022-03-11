from pymongo.errors import DuplicateKeyError

from backend.authentication.schemas import PyObjectId
from backend.core.database.driver import database
from backend.core.exception.base_exeption import UniqueIndexException

users_collection = database.get_collection("users")


class UserCrud:
    @staticmethod
    async def get(user_id: PyObjectId) -> dict:
        user = await users_collection.find_one({'_id': user_id})
        return user

    @staticmethod
    async def get_all() -> list:
        users = []
        async for user in users_collection.find():
            users.append(user)
        return users

    @staticmethod
    async def create(user: dict) -> str:
        try:
            user = await users_collection.insert_one(user)
            return str(user.inserted_id)
        except DuplicateKeyError as error:
            raise UniqueIndexException(error.details)

    @staticmethod
    async def update(user_id: PyObjectId, user: dict) -> str:
        try:
            user = await users_collection.update_one({'_id': user_id}, {'$set': user})
            return str(user.upserted_id)
        except DuplicateKeyError as error:
            raise UniqueIndexException(error.details)
