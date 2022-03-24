import json
from unittest import IsolatedAsyncioTestCase

from httpx import AsyncClient

from backend.tree.crud import NodeCrud
from backend.core.database.driver import init_database_client, get_database
from backend.main import app
from backend.user.crud import UserCrud


class NodeApiTestCase(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        init_database_client()
        self.connection = get_database()
        self.node_crud = NodeCrud()
        self.user_crud = UserCrud()

    async def asyncTearDown(self):
        await self.connection.database.get_collection("tree").delete_many({})
        await self.connection.database.get_collection("users").delete_many({})
        await self.connection.database.get_collection("refresh_tokens").delete_many({})
        self.connection.client.close()

    async def get_access_token(self, username: str, password: str, email: str):
        user = json.dumps({'username': username, 'password': password, 'email': email})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_register = await ac.post(f"/authentication/registration", data=user)
        user_id = response_register.content.decode("utf-8").replace('\"', '')
        await self.user_crud.update(user_id, {'active': True})
        auth_data = json.dumps({'username': username, 'password': password})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", data=auth_data)
        return json.loads(response_login.content)['access_token']

    async def test_get_node(self):
        node = await self.node_crud.create({'name': 'Максим', 'family_name': 'Бурень', 'father_name': 'Николаевич'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/tree/{node}")
        self.assertEqual(response.status_code, 200)
        node_data = json.loads(response.content)
        self.assertEqual(node_data['name'], 'Максим')
        self.assertEqual(node_data['family_name'], 'Бурень')
        self.assertEqual(node_data['father_name'], 'Николаевич')

    async def test_get_not_exist_node(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/tree/6231c1098d937d9ce2da8f20")
        self.assertEqual(response.status_code, 204)

    async def test_create_node(self):
        access_token = await self.get_access_token('andrey', '1ewuvn3i2344', 'pushkin@mail.com')
        node = json.dumps({'name': 'Максим', 'family_name': 'Бурень', 'father_name': 'Николаевич'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/tree/", data=node, headers={'x-access-token': access_token})
        self.assertEqual(response.status_code, 201)
        node_id = response.content.decode("utf-8").replace('\"', '')
        node_data = await self.node_crud.get(node_id)
        self.assertEqual(node_data['name'], 'Максим')
        self.assertEqual(node_data['family_name'], 'Бурень')
        self.assertEqual(node_data['father_name'], 'Николаевич')

    async def test_create_node_without_login(self):
        node = json.dumps({'name': 'Максим', 'family_name': 'Бурень', 'father_name': 'Николаевич'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/tree/", data=node)
        self.assertEqual(401, response.status_code)

    async def test_update_node(self):
        access_token = await self.get_access_token('andrey', '1ewuvn3i2344', 'pushkin@mail.com')
        node = json.dumps({'name': 'Максим', 'family_name': 'Бурень', 'father_name': 'Николаевич'})
        update_node = json.dumps({'father_name': 'Русланович'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            create_response = await ac.post(f"/tree/", data=node, headers={'x-access-token': access_token})
            node_id = create_response.content.decode("utf-8").replace('\"', '')
            update_response = await ac.put(f"/tree/{node_id}", data=update_node, headers={'x-access-token': access_token})
        self.assertEqual(update_response.status_code, 201)
        update_count = int(update_response.content.decode("utf-8").replace('\"', ''))
        self.assertEqual(update_count, 1)
        node_data = await self.node_crud.get(node_id)
        self.assertEqual(node_data['name'], 'Максим')
        self.assertEqual(node_data['family_name'], 'Бурень')
        self.assertEqual(node_data['father_name'], 'Русланович')

    async def test_update_node_without_login(self):
        access_token = await self.get_access_token('andrey', '1ewuvn3i2344', 'pushkin@mail.com')
        node = json.dumps({'name': 'Максим', 'family_name': 'Бурень', 'father_name': 'Николаевич'})
        update_node = json.dumps({'father_name': 'Русланович'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            create_response = await ac.post(f"/tree/", data=node, headers={'x-access-token': access_token})
            node_id = create_response.content.decode("utf-8").replace('\"', '')
            update_response = await ac.put(f"/tree/{node_id}", data=update_node)
        self.assertEqual(update_response.status_code, 401)
        node_data = await self.node_crud.get(node_id)
        self.assertEqual(node_data['father_name'], 'Николаевич')

    async def test_update_node_with_other_user(self):
        access_token_pushkin = await self.get_access_token('pushkin', '1ewuvn3i2344', 'pushkin@mail.com')
        access_token_andrey = await self.get_access_token('andrey', '1ewuvn3i2344', 'andrey@mail.com')
        node = json.dumps({'name': 'Максим', 'family_name': 'Бурень', 'father_name': 'Николаевич'})
        update_node = json.dumps({'father_name': 'Русланович'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            create_response = await ac.post(f"/tree/", data=node, headers={'x-access-token': access_token_pushkin})
            node_id = create_response.content.decode("utf-8").replace('\"', '')
            update_response = await ac.put(f"/tree/{node_id}", data=update_node, headers={'x-access-token': access_token_andrey})
        self.assertEqual(update_response.status_code, 403)
        node_data = await self.node_crud.get(node_id)
        self.assertEqual(node_data['father_name'], 'Николаевич')

    async def test_update_not_exist_node(self):
        access_token = await self.get_access_token('pushkin', '1ewuvn3i2344', 'pushkin@mail.com')
        update_node = json.dumps({'father_name': 'Русланович'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            update_response = await ac.put(f"/tree/6231c1098d937d9ce2da8f20", data=update_node, headers={'x-access-token': access_token})
        self.assertEqual(update_response.status_code, 404)

    async def test_update_node_without_update(self):
        access_token = await self.get_access_token('andrey', '1ewuvn3i2344', 'pushkin@mail.com')
        node = json.dumps({'name': 'Максим', 'family_name': 'Бурень', 'father_name': 'Николаевич'})
        update_node = json.dumps({'father_name': 'Николаевич'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            create_response = await ac.post(f"/tree/", data=node, headers={'x-access-token': access_token})
            node_id = create_response.content.decode("utf-8").replace('\"', '')
            update_response = await ac.put(f"/tree/{node_id}", data=update_node, headers={'x-access-token': access_token})
        self.assertEqual(update_response.status_code, 204)

    async def test_delete_node(self):
        access_token = await self.get_access_token('andrey', '1ewuvn3i2344', 'pushkin@mail.com')
        node = json.dumps({'name': 'Максим', 'family_name': 'Бурень', 'father_name': 'Николаевич'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            create_response = await ac.post(f"/tree/", data=node, headers={'x-access-token': access_token})
            node_id = create_response.content.decode("utf-8").replace('\"', '')
            update_response = await ac.delete(f"/tree/{node_id}", headers={'x-access-token': access_token})
        self.assertEqual(update_response.status_code, 200)
        database_node = await self.node_crud.get(node_id)
        self.assertIsNone(database_node)

    async def test_delete_node_without_login(self):
        access_token = await self.get_access_token('andrey', '1ewuvn3i2344', 'pushkin@mail.com')
        node = json.dumps({'name': 'Максим', 'family_name': 'Бурень', 'father_name': 'Николаевич'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            create_response = await ac.post(f"/tree/", data=node, headers={'x-access-token': access_token})
            node_id = create_response.content.decode("utf-8").replace('\"', '')
            update_response = await ac.delete(f"/tree/{node_id}")
        self.assertEqual(update_response.status_code, 401)
        database_node = await self.node_crud.get(node_id)
        self.assertEqual(database_node['name'], 'Максим')
        self.assertEqual(database_node['family_name'], 'Бурень')
        self.assertEqual(database_node['father_name'], 'Николаевич')

    async def test_delete_node_with_other_user(self):
        access_token_pushkin = await self.get_access_token('pushkin', '1ewuvn3i2344', 'pushkin@mail.com')
        access_token_andrey = await self.get_access_token('andrey', '1ewuvn3i2344', 'andrey@mail.com')
        node = json.dumps({'name': 'Максим', 'family_name': 'Бурень', 'father_name': 'Николаевич'})
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            create_response = await ac.post(f"/tree/", data=node, headers={'x-access-token': access_token_pushkin})
            node_id = create_response.content.decode("utf-8").replace('\"', '')
            update_response = await ac.delete(f"/tree/{node_id}", headers={'x-access-token': access_token_andrey})
        self.assertEqual(update_response.status_code, 403)
        node_data = await self.node_crud.get(node_id)
        self.assertEqual(node_data['name'], 'Максим')
        self.assertEqual(node_data['family_name'], 'Бурень')
        self.assertEqual(node_data['father_name'], 'Николаевич')

    async def test_delete_not_exist_node(self):
        access_token = await self.get_access_token('pushkin', '1ewuvn3i2344', 'pushkin@mail.com')
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            update_response = await ac.delete(f"/tree/6231c1098d937d9ce2da8f20", headers={'x-access-token': access_token})
        self.assertEqual(update_response.status_code, 404)