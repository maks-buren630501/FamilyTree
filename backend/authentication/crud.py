from core.database.crud import BaseCrud


class RefreshTokenCrud(BaseCrud):
    def __init__(self):
        super().__init__("refresh_tokens")

    async def get_by_user_id(self, user_id: str) -> list:
        tokens = []
        async for token in self._collection.find({'user_id': user_id}):
            tokens.append(BaseCrud._stringify_id(token))
        return tokens
