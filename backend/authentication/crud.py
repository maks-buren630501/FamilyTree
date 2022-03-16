from backend.core.database.crud import BaseCrud


class UserCrud(BaseCrud):

    def __init__(self):
        super().__init__("users")

    async def find(self, find_data):
        user = await self._collection.find_one(find_data)
        if user:
            return self._stringify_id(user)
        else:
            return None

