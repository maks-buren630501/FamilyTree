# import json
# from unittest import IsolatedAsyncioTestCase
#
# from httpx import AsyncClient
#
# from authentication.crud import RefreshTokenCrud
# from core.database.driver import init_database_client, get_database
# from main import app
# from user.crud import UserCrud
#
#
# class AuthenticationApiTestCase(IsolatedAsyncioTestCase):
#
#     async def asyncSetUp(self):
#         init_database_client()
#         self.connection = get_database()
#         self.user_crud = UserCrud()
#         self.token_crud = RefreshTokenCrud()
#
#     async def asyncTearDown(self):
#         await self.connection.database.get_collection("users").delete_many({})
#         await self.connection.database.get_collection("refresh_tokens").delete_many({})
#         self.connection.client.close()
#
#     async def test_register_user(self):
#         user = json.dumps({'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'andrey@mail.com'})
#         async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#             response = await ac.post(f"/authentication/registration", data=user)
#         self.assertEqual(response.status_code, 201)
#         user_id = response.content.decode("utf-8").replace('\"', '')
#         database_user = await self.user_crud.get(user_id)
#         self.assertEqual(database_user['username'], 'andrey')
#
#     async def test_register_user_with_same_email(self):
#         await self.user_crud.create({'username': 'pushkin', 'email': 'pushkin@mail.com', 'password': b'veverbi344'})
#         user = json.dumps({'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'pushkin@mail.com'})
#         async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#             response = await ac.post(f"/authentication/registration", data=user)
#         self.assertEqual(response.status_code, 409)
#
#     async def test_register_user_with_short_password(self):
#         user = json.dumps({'username': 'andrey', 'password': '1234567', 'email': 'pushkin@mail.com'})
#         async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#             response = await ac.post(f"/authentication/registration", data=user)
#         self.assertEqual(response.status_code, 406)
#
#     async def test_register_user_with_short_name(self):
#         user = json.dumps({'username': 'and', 'password': '12345678910', 'email': 'pushkin@mail.com'})
#         async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#             response = await ac.post(f"/authentication/registration", data=user)
#         self.assertEqual(response.status_code, 406)
#
#     async def test_login(self):
#         user = json.dumps({'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'pushkin@mail.com'})
#         async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#             response_register = await ac.post(f"/authentication/registration", data=user)
#         user_id = response_register.content.decode("utf-8").replace('\"', '')
#         await self.user_crud.update(user_id, {'active': True})
#         auth_data = json.dumps({'username': 'andrey', 'password': '1ewuvn3i2344'})
#         async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#             response_login = await ac.post(f"/authentication/login", data=auth_data)
#         self.assertEqual(response_login.status_code, 200)
#
#     async def test_login_no_active_user(self):
#         user = json.dumps({'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'pushkin@mail.com'})
#         async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#             response_register = await ac.post(f"/authentication/registration", data=user)
#         auth_data = json.dumps({'username': 'andrey', 'password': '1ewuvn3i2344'})
#         async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#             response_login = await ac.post(f"/authentication/login", data=auth_data)
#         self.assertEqual(response_login.status_code, 403)
#
#     async def test_login_with_wrong_password(self):
#         user = json.dumps({'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'pushkin@mail.com'})
#         async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#             response_register = await ac.post(f"/authentication/registration", data=user)
#         user_id = response_register.content.decode("utf-8").replace('\"', '')
#         await self.user_crud.update(user_id, {'active': True})
#         auth_data = json.dumps({'username': 'andrey', 'password': '235431brgb'})
#         async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#             response_login = await ac.post(f"/authentication/login", data=auth_data)
#         self.assertEqual(response_login.status_code, 403)
#
#     async def test_login_with_wrong_username(self):
#         user = json.dumps({'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'pushkin@mail.com'})
#         async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#             response_register = await ac.post(f"/authentication/registration", data=user)
#         user_id = response_register.content.decode("utf-8").replace('\"', '')
#         await self.user_crud.update(user_id, {'active': True})
#         auth_data = json.dumps({'username': 'pushkin', 'password': '1ewuvn3i2344'})
#         async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#             response_login = await ac.post(f"/authentication/login", data=auth_data)
#         self.assertEqual(response_login.status_code, 403)
#
#     async def test_refresh(self):
#         user = json.dumps({'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'pushkin@mail.com'})
#         async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#             response_register = await ac.post(f"/authentication/registration", data=user)
#         user_id = response_register.content.decode("utf-8").replace('\"', '')
#         await self.user_crud.update(user_id, {'active': True})
#         auth_data = json.dumps({'username': 'andrey', 'password': '1ewuvn3i2344'})
#         async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#             await ac.post(f"/authentication/login", data=auth_data)
#             response_refresh = await ac.get(f"/authentication/refresh")
#         self.assertEqual(response_refresh.status_code, 200)
#
#     async def test_refresh_without_cookies(self):
#         async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#             response_refresh = await ac.get(f"/authentication/refresh")
#         self.assertEqual(response_refresh.status_code, 403)
#
#     async def test_logout(self):
#         user = json.dumps({'username': 'andrey', 'password': '1ewuvn3i2344', 'email': 'pushkin@mail.com'})
#         async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#             response_register = await ac.post(f"/authentication/registration", data=user)
#         user_id = response_register.content.decode("utf-8").replace('\"', '')
#         await self.user_crud.update(user_id, {'active': True})
#         auth_data = json.dumps({'username': 'andrey', 'password': '1ewuvn3i2344'})
#         async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#             response_login = await ac.post(f"/authentication/login", data=auth_data)
#             response_data = json.loads(response_login.content)
#             response_logout = await ac.get(f"/authentication/logout", headers={'x-access-token': response_data['access_token']})
#         self.assertEqual(response_logout.status_code, 200)
#
#
#
