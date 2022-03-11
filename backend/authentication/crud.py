from bson import ObjectId
from bson.errors import InvalidId

from pymongo.errors import DuplicateKeyError

from backend.core.database.driver import database
from backend.core.exception.base_exeption import UniqueIndexException


users_collection = database.get_collection("users")


class UserCrud:

    @classmethod
    def __convert_url(cls, item_id: str) -> ObjectId | None:
        try:
            return ObjectId(item_id)
        except InvalidId:
            return None

    @classmethod
    def __stringify_id(cls, payload: dict | ObjectId) -> str | dict:
        if isinstance(payload, dict):
            payload['id'] = str(payload['_id'])
            del payload['_id']
            return payload
        elif isinstance(payload, ObjectId):
            return str(payload)

    @staticmethod
    async def get(user_id: str) -> dict | None:
        user_id = UserCrud.__convert_url(user_id)
        if not user_id:
            return None
        user = await users_collection.find_one({'_id': user_id})
        return UserCrud.__stringify_id(user)

    @staticmethod
    async def get_all() -> list:
        users = []
        async for user in users_collection.find():
            users.append(UserCrud.__stringify_id(user))
        return users

    @staticmethod
    async def create(user: dict) -> str:
        try:
            user = await users_collection.insert_one(user)
            return UserCrud.__stringify_id(user.inserted_id)
        except DuplicateKeyError as e:
            raise UniqueIndexException(e.details)

    @staticmethod
    async def update(user_id: str, user: dict) -> int | None:
        user_id = UserCrud.__convert_url(user_id)
        if not user_id:
            return None
        try:
            result = await users_collection.update_one({'_id': user_id}, {'$set': user})
            if not result.raw_result['updatedExisting']:
                return None
            return result.modified_count
        except DuplicateKeyError as e:
            raise UniqueIndexException(e.details)

    @staticmethod
    async def delete(user_id: str) -> int | None:
        user_id = UserCrud.__convert_url(user_id)
        result = await users_collection.delete_one({'_id': user_id})
        if result.deleted_count:
            return result.deleted_count
        else:
            return None
