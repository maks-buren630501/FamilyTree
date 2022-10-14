import json
from unittest import IsolatedAsyncioTestCase

from httpx import AsyncClient

from user.crud import UserCrud
from core.database.driver import init_database_client, get_database
from main import app


class UserApiTestCase(IsolatedAsyncioTestCase):

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
            response = await ac.get(f"/user/{user}")
        self.assertEqual(response.status_code, 200)
        user_data = json.loads(response.content)
        self.assertEqual(user_data['username'], 'pushkin')
        self.assertEqual(user_data['email'], 'pushkin@mail.com')

    async def test_get_not_exist_user(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/user/6231c1098d937d9ce2da8f20")
        self.assertEqual(response.status_code, 204)

    async def test_create_user(self):
        user = json.dumps({'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'andrey@mail.com'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/user/", data=user)
        self.assertEqual(response.status_code, 201)
        user_id = response.content.decode("utf-8").replace('\"','')
        database_user = await self.crud.get(user_id)
        self.assertEqual(database_user['username'], 'andrey')

    async def test_create_user_with_same_email(self):
        await self.crud.create({'username': 'pushkin', 'email': 'pushkin@mail.com', 'password': b'veverbi344'})
        user = json.dumps({'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'pushkin@mail.com'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/user/", data=user)
        self.assertEqual(response.status_code, 409)

    async def test_create_user_with_short_password(self):
        user = json.dumps({'username': 'andrey', 'password': '1234567', 'email': 'pushkin@mail.com'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/user/", data=user)
        self.assertEqual(response.status_code, 406)

    async def test_create_user_with_short_name(self):
        user = json.dumps({'username': 'and', 'password': '12345678910', 'email': 'pushkin@mail.com'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/user/", data=user)
        self.assertEqual(response.status_code, 406)

    async def test_get_users(self):
        await self.crud.create({'username': 'andrey', 'email': 'andrey@mail.com', 'password': b'veverrgbrbbi344'})
        await self.crud.create({'username': 'pushkin', 'email': 'pushkin@mail.com', 'password': b'veverbi344'})
        await self.crud.create({'username': 'roman', 'email': 'roman@mail.com', 'password': b'wfvvw4r2fveffv'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/user/")
        self.assertEqual(response.status_code, 200)
        user_data = json.loads(response.content)
        self.assertIsInstance(user_data, list)
        self.assertEqual(3, len(user_data))

    async def test_get_empty_users(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/user/")
        self.assertEqual(response.status_code, 200)
        user_data = json.loads(response.content)
        self.assertIsInstance(user_data, list)
        self.assertEqual(0, len(user_data))

    async def test_update_user(self):
        user_id = await self.crud.create({'username': 'pushkin', 'email': 'andrey@mail.com', 'password': b'vevrbbi344'})
        data = json.dumps({'username': 'andrey'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.put(f"/user/{user_id}", data=data)
        self.assertEqual(response.status_code, 201)
        update_count = int(response.content.decode("utf-8").replace('\"',''))
        self.assertEqual(update_count, 1)
        database_user = await self.crud.get(user_id)
        self.assertEqual(database_user['username'], 'andrey')

    async def test_update_not_exist_user(self):
        data = json.dumps({'username': 'andrey'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.put(f"/user/6231c1098d937d9ce2da8f20", data=data)
        self.assertEqual(response.status_code, 204)

    async def test_update_user_with_same_email(self):
        await self.crud.create({'username': 'pushkin', 'email': 'pushkin@mail.com', 'password': b'veverrgbrbbi344'})
        user_id = await self.crud.create({'username': 'andrey', 'email': 'andrey@mail.com', 'password': b'rb4gt4gbtrb'})
        data = json.dumps({'email': 'pushkin@mail.com'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.put(f"/user/{user_id}", data=data)
        self.assertEqual(response.status_code, 409)

    async def test_delete_user(self):
        user_id = await self.crud.create({'username': 'pushkin', 'email': 'andrey@mail.com', 'password': b'vevrbbi344'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.delete(f"/user/{user_id}")
        self.assertEqual(response.status_code, 200)
        delete_count = int(response.content.decode("utf-8").replace('\"',''))
        self.assertEqual(delete_count, 1)
        database_user = await self.crud.get(user_id)
        self.assertIsNone(database_user)

    async def test_delete_not_exist_user(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.delete(f"/user/6231c1098d937d9ce2da8f20")
        self.assertEqual(response.status_code, 204)





