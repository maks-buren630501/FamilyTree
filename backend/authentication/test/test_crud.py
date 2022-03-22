from unittest import IsolatedAsyncioTestCase

from backend.authentication.crud import RefreshTokenCrud
from backend.authentication.functions import create_refresh_token
from backend.core.database.driver import init_database_client, get_database


class AuthenticationCrudTestCase(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        init_database_client()
        self.connection = get_database()
        self.crud = RefreshTokenCrud()

    async def asyncTearDown(self):
        await self.connection.database.get_collection("refresh_tokens").delete_many({})
        self.connection.client.close()

    async def test_get_refresh_token_by_id(self):
        token = await self.crud.create(create_refresh_token('622db5ecf978a3e718b61934').dict())
        token_data = await self.crud.get(token)
        self.assertEqual(token_data['user_id'], '622db5ecf978a3e718b61934')

    async def test_get_not_exist_token(self):
        user_data = await self.crud.get('622db5ecf978a3e718b61933')
        self.assertIsNone(user_data)

    async def test_get_all_tokens(self):
        await self.crud.create(create_refresh_token('622db5ecf978a3e718b61935').dict())
        await self.crud.create(create_refresh_token('622db5ecf978a3e718b61936').dict())
        await self.crud.create(create_refresh_token('622db5ecf978a3e718b61937').dict())
        tokens = await self.crud.get_all()
        self.assertIsInstance(tokens, list)
        self.assertEqual(3, len(tokens))

    async def test_remove_token(self):
        await self.crud.create(create_refresh_token('622db5ecf978a3e718b61935').dict())
        token = await self.crud.create(create_refresh_token('622db5ecf978a3e718b61936').dict())
        result = await self.crud.delete(token)
        users = await self.crud.get_all()
        self.assertEqual(1, len(users))
        self.assertEqual(result, 1)

    async def test_remove_not_exist_token(self):
        result = await self.crud.delete('622db5ecf978a3e718b61935')
        self.assertIsNone(result)

    async def test_find_token(self):
        await self.crud.create(create_refresh_token('622db5ecf978a3e718b61935').dict())
        await self.crud.create(create_refresh_token('622db5ecf978a3e718b61935').dict())
        tokens = await self.crud.get_by_user_id('622db5ecf978a3e718b61935')
        self.assertIsInstance(tokens, list)
        self.assertEqual(2, len(tokens))

    async def test_find_not_exist_token(self):
        await self.crud.create(create_refresh_token('622db5ecf978a3e718b61935').dict())
        tokens = await self.crud.get_by_user_id('622db5ecf978a3e718b61936')
        self.assertIsInstance(tokens, list)
        self.assertEqual(0, len(tokens))

