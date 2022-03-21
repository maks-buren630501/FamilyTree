import json
from unittest import IsolatedAsyncioTestCase

from httpx import AsyncClient

from backend.authentication.crud import UserCrud
from backend.core.database.driver import init_database_client, get_database
from backend.main import app


class UserCrudTestCase(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        init_database_client()
        self.connection = get_database()
        self.crud = UserCrud()

    async def asyncTearDown(self):
        await self.connection.database.get_collection("users").delete_many({})
        self.connection.client.close()

    async def test_get_user(self):
        user = await self.crud.create({'username': 'pushkin', 'email': 'pushkin@mail.com', 'password': b'veverbi344'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/authentication/{user}")
        self.assertEqual(response.status_code, 200)
        user_data = json.loads(response.content)
        self.assertEqual(user_data['username'], 'pushkin')
        self.assertEqual(user_data['email'], 'pushkin@mail.com')

    async def test_get_not_exist_user(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/authentication/6231c1098d937d9ce2da8f20")
        self.assertEqual(response.status_code, 204)
