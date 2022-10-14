from tree.crud import NodeCrud
from core.database.driver import init_database_client, get_database

from unittest import IsolatedAsyncioTestCase

from core.exception.base_exeption import UniqueIndexException


class NodeCrudTestCase(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        init_database_client()
        self.connection = get_database()
        self.crud = NodeCrud()

    async def asyncTearDown(self):
        await self.connection.database.get_collection("tree").delete_many({})
        self.connection.client.close()

    async def test_get_node_by_id(self):
        node = await self.crud.create({'name': 'Максим', 'family_name': 'Бурень', 'father_name': 'Николаевич'})
        node_data = await self.crud.get(node)
        self.assertEqual(node_data['name'], 'Максим')
        self.assertEqual(node_data['family_name'], 'Бурень')
        self.assertEqual(node_data['father_name'], 'Николаевич')

    async def test_get_user_by_wroregistrationng_id(self):
        node_data = await self.crud.get('2437328459ettb')
        self.assertIsNone(node_data)

    async def test_get_not_exist_user(self):
        node_data = await self.crud.get('622db5ecf978a3e718b61933')
        self.assertIsNone(node_data)

    async def test_remove_node(self):
        first_node = await self.crud.create({'name': 'Максим', 'family_name': 'Бурень', 'father_name': 'Николаевич'})
        second_node = node = await self.crud.create({'name': 'Кирилл', 'family_name': 'Стасюк', 'father_name': 'Андреевич'})
        result = await self.crud.delete(second_node)
        first_node = await self.crud.get(first_node)
        second_node = await self.crud.get(second_node)
        self.assertIsNone(second_node)
        self.assertEqual(first_node['name'], 'Максим')
        self.assertEqual(first_node['family_name'], 'Бурень')
        self.assertEqual(first_node['father_name'], 'Николаевич')

    async def test_remove_node_with_wrong_id(self):
        result = await self.crud.delete('2437328459ettbfe')
        self.assertIsNone(result)

    async def test_remove_not_exist_node(self):
        result = await self.crud.delete('622db5ecf978a3e718b61934')
        self.assertIsNone(result)





