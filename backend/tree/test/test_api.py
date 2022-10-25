import datetime
import json
from unittest import IsolatedAsyncioTestCase

from httpx import AsyncClient
from sqlmodel import select

from authentication.functions import hash_password
from core.database.crud import Crud
from core.database.migrations import clear_tables
from main import app
from tree.models import NodeDataBase, PartnersMapper, NodeSchemaUpdate, BaseNodeSchema
from user.models import UserDataBase


class TreeApiTestCase(IsolatedAsyncioTestCase):

    async def asyncTearDown(self):
        await clear_tables()

    async def test_get_node(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        node = await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user))
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/tree/{node}")
        self.assertEqual(response.status_code, 200)
        node_data = json.loads(response.content)
        self.assertEqual(node_data['name'], 'Andrey')
        self.assertEqual(node_data['family_name'], 'Bichkoy')

    async def test_not_exist_node(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/tree/b20a34ab-c9e9-436a-bf14-e91973614d60")
        self.assertEqual(response.status_code, 204)

    async def test_get_node_with_partner(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        node_1 = await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user))
        node_2 = await Crud.save(NodeDataBase(name='Irina', family_name='Bichkoy', author_id=user))
        await Crud.save(PartnersMapper(husband_id=node_1, wife_id=node_2, wedding_date=datetime.date(2000, 1, 1)))
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/tree/{node_1}")
        self.assertEqual(response.status_code, 200)
        node_data = json.loads(response.content)
        self.assertEqual(node_data['name'], 'Andrey')
        self.assertEqual(node_data['family_name'], 'Bichkoy')
        self.assertEqual(node_data['partners'][0]['partner_id'], str(node_2))

    async def test_get_nodes(self):
        user_1 = await Crud.save(UserDataBase(username='pushkin', password=hash_password('1ewuvn3i2344'), email='pushkin@mail.com', active=True))
        user_2 = await Crud.save(UserDataBase(username='zero', password=b'veverbi344', email='zero@mail.com'))
        await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user_1))
        await Crud.save(NodeDataBase(name='Dima', family_name='Bichkoy', author_id=user_1))
        await Crud.save(NodeDataBase(name='Petr', family_name='Trifonov', author_id=user_2))
        auth_data = {'username': 'pushkin', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        token = json.loads(response_login.content)['access_token']
        async with AsyncClient(app=app, base_url="http://127.0.0.1", headers={'x-access-token': token}) as ac:
            response = await ac.get(f"/tree/")
        self.assertEqual(response.status_code, 200)
        node_data = json.loads(response.content)
        self.assertEqual(len(node_data), 2)

    async def test_get_nodes_no_authentication(self):
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/tree/")
        self.assertEqual(response.status_code, 401)

    async def test_search_nodes(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=hash_password('1ewuvn3i2344'), email='pushkin@mail.com'))
        await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user))
        await Crud.save(NodeDataBase(name='Dima', family_name='Bichkoy', author_id=user))
        await Crud.save(NodeDataBase(name='Petr', family_name='Trifonov', author_id=user))
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/tree/search/Bichkoy")
        self.assertEqual(response.status_code, 200)
        node_data = json.loads(response.content)
        self.assertEqual(len(node_data), 2)
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/tree/search/Petr Trifonov")
        self.assertEqual(response.status_code, 200)
        node_data = json.loads(response.content)
        self.assertEqual(len(node_data), 1)

    async def test_find_nodes(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=hash_password('1ewuvn3i2344'), email='pushkin@mail.com'))
        await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user))
        await Crud.save(NodeDataBase(name='Dima', family_name='Bichkoy', author_id=user))
        await Crud.save(NodeDataBase(name='Petr', family_name='Trifonov', author_id=user))
        node_to_find = NodeSchemaUpdate(name='Dima', family_name='Bichkoy', author_id=user).dict(exclude_unset=True)
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/tree/find", json=node_to_find)
        self.assertEqual(response.status_code, 200)
        node_data = json.loads(response.content)
        self.assertEqual(len(node_data), 1)

    async def test_get_children(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=hash_password('1ewuvn3i2344'), email='pushkin@mail.com'))
        node_id = await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user))
        await Crud.save(NodeDataBase(name='Dima', family_name='Bichkoy', author_id=user, father_id=node_id))
        await Crud.save(NodeDataBase(name='Petr', family_name='Bichkoy', author_id=user, father_id=node_id))
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.get(f"/tree/children/{node_id}")
        self.assertEqual(response.status_code, 200)
        node_data = json.loads(response.content)
        self.assertEqual(len(node_data), 2)
        for node in node_data:
            self.assertEqual(node['father_id'], str(node_id))

    async def test_create_node(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=hash_password('1ewuvn3i2344'), email='pushkin@mail.com', active=True))
        node = BaseNodeSchema(name='Andrey', family_name='Bichkoy', author_id=user)
        auth_data = {'username': 'pushkin', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        token = json.loads(response_login.content)['access_token']
        async with AsyncClient(app=app, base_url="http://127.0.0.1", headers={'x-access-token': token}) as ac:
            response = await ac.post(f"/tree/", json=node.dict(exclude_unset=True))
        self.assertEqual(response.status_code, 201)
        node_id = json.loads(response.content)
        node_database: NodeDataBase = await Crud.get(select(NodeDataBase).where(NodeDataBase.id == node_id))
        self.assertEqual(node_database.name, 'Andrey')

    async def test_create_node_no_authentication(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=hash_password('1ewuvn3i2344'), email='pushkin@mail.com'))
        node = BaseNodeSchema(name='Andrey', family_name='Bichkoy', author_id=user)
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.post(f"/tree/", json=node.dict(exclude_unset=True))
        self.assertEqual(response.status_code, 401)

    async def test_update_node(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=hash_password('1ewuvn3i2344'), email='pushkin@mail.com', active=True))
        node = await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user))
        node_update = NodeSchemaUpdate(name='Dima')
        auth_data = {'username': 'pushkin', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        token = json.loads(response_login.content)['access_token']
        async with AsyncClient(app=app, base_url="http://127.0.0.1", headers={'x-access-token': token}) as ac:
            response = await ac.put(f"/tree/{node}", json=node_update.dict(exclude_unset=True))
        self.assertEqual(response.status_code, 201)
        node_database: NodeDataBase = await Crud.get(select(NodeDataBase).where(NodeDataBase.id == node))
        self.assertEqual(node_database.name, 'Dima')

    async def test_update_node_no_authentication(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=hash_password('1ewuvn3i2344'), email='pushkin@mail.com'))
        node = await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user))
        node_update = NodeSchemaUpdate(name='Dima')
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.put(f"/tree/{node}", json=node_update.dict(exclude_unset=True))
        self.assertEqual(response.status_code, 401)

    async def test_update_by_other_user(self):
        await Crud.save(UserDataBase(username='pushkin', password=hash_password('1ewuvn3i2344'), email='pushkin@mail.com', active=True))
        user_2 = await Crud.save(UserDataBase(username='zero', password=hash_password('1ewuvn3i2344'), email='zero@mail.com', active=True))
        node = await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user_2))
        node_update = NodeSchemaUpdate(name='Dima')
        auth_data = {'username': 'pushkin', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        token = json.loads(response_login.content)['access_token']
        async with AsyncClient(app=app, base_url="http://127.0.0.1", headers={'x-access-token': token}) as ac:
            response = await ac.put(f"/tree/{node}", json=node_update.dict(exclude_unset=True))
        self.assertEqual(response.status_code, 403)

    async def test_update_not_exist_node(self):
        await Crud.save(UserDataBase(username='pushkin', password=hash_password('1ewuvn3i2344'), email='pushkin@mail.com', active=True))
        node_update = NodeSchemaUpdate(name='Dima')
        auth_data = {'username': 'pushkin', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        token = json.loads(response_login.content)['access_token']
        async with AsyncClient(app=app, base_url="http://127.0.0.1", headers={'x-access-token': token}) as ac:
            response = await ac.put(f"/tree/b4c0f731-1761-46e2-8751-c567ca12cda8", json=node_update.dict(exclude_unset=True))
        self.assertEqual(response.status_code, 204)

    async def test_delete_node(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=hash_password('1ewuvn3i2344'), email='pushkin@mail.com', active=True))
        node = await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user))
        auth_data = {'username': 'pushkin', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        token = json.loads(response_login.content)['access_token']
        async with AsyncClient(app=app, base_url="http://127.0.0.1", headers={'x-access-token': token}) as ac:
            response = await ac.delete(f"/tree/{node}")
        self.assertEqual(response.status_code, 200)

    async def test_delete_by_other_user(self):
        await Crud.save(UserDataBase(username='pushkin', password=hash_password('1ewuvn3i2344'), email='pushkin@mail.com', active=True))
        user_2 = await Crud.save(UserDataBase(username='zero', password=hash_password('1ewuvn3i2344'), email='zero@mail.com', active=True))
        node = await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user_2))
        auth_data = {'username': 'pushkin', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        token = json.loads(response_login.content)['access_token']
        async with AsyncClient(app=app, base_url="http://127.0.0.1", headers={'x-access-token': token}) as ac:
            response = await ac.delete(f"/tree/{node}")
        self.assertEqual(response.status_code, 403)

    async def test_delete_node_no_authentication(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=hash_password('1ewuvn3i2344'), email='pushkin@mail.com'))
        node_id = await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user))
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response = await ac.delete(f"/tree/{node_id}")
        self.assertEqual(response.status_code, 401)
        node: NodeDataBase = await Crud.get(select(NodeDataBase).where(NodeDataBase.id == node_id))
        self.assertEqual(node.name, 'Andrey')

    async def test_delete_not_exist_node(self):
        await Crud.save(UserDataBase(username='pushkin', password=hash_password('1ewuvn3i2344'), email='pushkin@mail.com', active=True))
        auth_data = {'username': 'pushkin', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        token = json.loads(response_login.content)['access_token']
        async with AsyncClient(app=app, base_url="http://127.0.0.1", headers={'x-access-token': token}) as ac:
            response = await ac.delete(f"/tree/b4c0f731-1761-46e2-8751-c567ca12cda8")
        self.assertEqual(response.status_code, 204)

    async def test_create_partners(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=hash_password('1ewuvn3i2344'), email='pushkin@mail.com', active=True))
        node_1 = await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user))
        node_2 = await Crud.save(NodeDataBase(name='Irina', family_name='Bichkoy', author_id=user))
        data = {'husband_id': str(node_1), 'wife_id': str(node_2), 'wedding_date': str(datetime.date(2020,1,1))}
        auth_data = {'username': 'pushkin', 'password': '1ewuvn3i2344'}
        async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
            response_login = await ac.post(f"/authentication/login", json=auth_data)
        token = json.loads(response_login.content)['access_token']
        async with AsyncClient(app=app, base_url="http://127.0.0.1", headers={'x-access-token': token}) as ac:
            response = await ac.post(f"/tree/partner", json=data)
            response_node = await ac.get(f"/tree/{node_1}")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_node.status_code, 200)
        node = json.loads(response_node.content)
        self.assertEqual(node['partners'][0]['partner_id'], str(node_2))











