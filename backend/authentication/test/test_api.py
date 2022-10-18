import json
from unittest import IsolatedAsyncioTestCase

from httpx import AsyncClient
from sqlmodel import select

from core.database.crud import Crud
from core.database.driver import init_db
from core.database.migrations import clear_tables
from main import app
from user.models import UserDataBase


class AuthenticationApiTestCase(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        init_db()

    async def asyncTearDown(self):
        await clear_tables()

    async def test_register_user(self):
        user = {'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'andrey@mail.com'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/authentication/registration", json=user)
        self.assertEqual(response.status_code, 201)
        user_id = response.content.decode("utf-8").replace('\"', '')
        database_user: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        self.assertEqual(database_user.username, 'andrey')

    async def test_register_user_with_same_email(self):
        await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        user = {'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'pushkin@mail.com'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/authentication/registration", json=user)
        self.assertEqual(response.status_code, 409)

    async def test_register_user_with_short_password(self):
        user = {'username': 'andrey', 'password': '1234567', 'email': 'pushkin@mail.com'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/authentication/registration", json=user)
        self.assertEqual(response.status_code, 406)

    async def test_register_user_with_short_name(self):
        user = {'username': 'and', 'password': '12345678910', 'email': 'pushkin@mail.com'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/authentication/registration", json=user)
        self.assertEqual(response.status_code, 406)

    async def test_login(self):
        user = {'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'pushkin@mail.com'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_register = await ac.post(f"/authentication/registration", json=user)
        user_id = response_register.content.decode("utf-8").replace('\"', '')
        user_database: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        user_database.active = True
        await Crud.save(user_database)
        auth_data = {'username': 'andrey', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        self.assertEqual(response_login.status_code, 200)

    async def test_login_no_active_user(self):
        user = {'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'pushkin@mail.com'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            await ac.post(f"/authentication/registration", json=user)
        auth_data = {'username': 'andrey', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        self.assertEqual(response_login.status_code, 403)

    async def test_login_with_wrong_password(self):
        user = {'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'pushkin@mail.com'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_register = await ac.post(f"/authentication/registration", json=user)
        user_id = response_register.content.decode("utf-8").replace('\"', '')
        user_database: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        user_database.active = True
        await Crud.save(user_database)
        auth_data = {'username': 'andrey', 'password': '235431brgb'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        self.assertEqual(response_login.status_code, 403)

    async def test_login_with_wrong_username(self):
        user = {'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'pushkin@mail.com'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_register = await ac.post(f"/authentication/registration", json=user)
        user_id = response_register.content.decode("utf-8").replace('\"', '')
        user_database: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        user_database.active = True
        await Crud.save(user_database)
        auth_data = {'username': 'pushkin', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        self.assertEqual(response_login.status_code, 403)

    async def test_refresh(self):
        user = {'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'pushkin@mail.com'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_register = await ac.post(f"/authentication/registration", json=user)
        user_id = response_register.content.decode("utf-8").replace('\"', '')
        user_database: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        user_database.active = True
        await Crud.save(user_database)
        auth_data = {'username': 'andrey', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            await ac.post(f"/authentication/login", json=auth_data)
            response_refresh = await ac.get(f"/authentication/refresh")
        self.assertEqual(response_refresh.status_code, 200)

    async def test_refresh_without_cookies(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_refresh = await ac.get(f"/authentication/refresh")
        self.assertEqual(response_refresh.status_code, 403)

    async def test_logout(self):
        user = {'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'pushkin@mail.com'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_register = await ac.post(f"/authentication/registration", json=user)
        user_id = response_register.content.decode("utf-8").replace('\"', '')
        user_database: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        user_database.active = True
        await Crud.save(user_database)
        auth_data = {'username': 'andrey', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
            response_data = json.loads(response_login.content)
            response_logout = await ac.get(f"/authentication/logout", headers={'x-access-token': response_data['access_token']})
        self.assertEqual(response_logout.status_code, 200)



