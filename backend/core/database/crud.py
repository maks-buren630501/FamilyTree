from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError

from core.database.driver import get_database
from core.exception.base_exeption import UniqueIndexException


class BaseCrud:

    def __init__(self, name: str):
        self._connection = get_database()
        self._collection = self._connection.database.get_collection(name)

    @classmethod
    def _convert_id(cls, item_id: str) -> ObjectId | None:
        try:
            return ObjectId(item_id)
        except InvalidId:
            return None

    @classmethod
    def _stringify_id(cls, payload: dict | ObjectId) -> str | dict:
        if isinstance(payload, dict):
            payload['id'] = str(payload['_id'])
            del payload['_id']
            return payload
        elif isinstance(payload, ObjectId):
            return str(payload)

    async def get(self, user_id: str) -> dict | None:
        document_id = BaseCrud._convert_id(user_id)
        if not document_id:
            return None
        user = await self._collection.find_one({'_id': document_id})
        return BaseCrud._stringify_id(user)

    async def get_all(self) -> list:
        documents = []
        async for document in self._collection.find():
            documents.append(BaseCrud._stringify_id(document))
        return documents

    async def create(self, document: dict) -> str:
        try:
            find_document = await self._collection.insert_one(document)
            return BaseCrud._stringify_id(find_document.inserted_id)
        except DuplicateKeyError as e:
            raise UniqueIndexException(e.details)

    async def update(self, document_id: str, document: dict) -> int | None:
        document_id = self._convert_id(document_id)
        if not document_id:
            return None
        try:
            result = await self._collection.update_one({'_id': document_id}, {'$set': document})
            if not result.raw_result['updatedExisting']:
                return None
            return result.modified_count
        except DuplicateKeyError as e:
            raise UniqueIndexException(e.details)

    async def delete(self, document_id: str) -> int | None:
        document_id = BaseCrud._convert_id(document_id)
        result = await self._collection.delete_one({'_id': document_id})
        if result.deleted_count:
            return result.deleted_count
        else:
            return None
