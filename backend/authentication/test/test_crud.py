from backend.authentication.crud import UserCrud
from backend.core.database.driver import init_database_client, get_database

from unittest import IsolatedAsyncioTestCase

from backend.core.exception.base_exeption import UniqueIndexException


class UserCrudTestCase(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        init_database_client(name='testFamilyTree')
        self.connection = get_database()
        self.crud = UserCrud()

    async def asyncTearDown(self):
        await self.connection.database.get_collection("users").delete_many({})
        self.connection.client.close()

    async def test_get_user_by_id(self):
        user = await self.crud.create({'name': 'pushkin', 'email': 'pushkin@mail.com', 'password': 'veverbi344'})
        user_data = await self.crud.get(user)
        self.assertEqual(user_data['name'], 'pushkin')
        self.assertEqual(user_data['email'], 'pushkin@mail.com')
        self.assertEqual(user_data['password'], 'veverbi344')

    async def test_get_user_by_wrong_id(self):
        user_data = await self.crud.get('2437328459ettb')
        self.assertIsNone(user_data)

    async def test_get_not_exist_user(self):
        user_data = await self.crud.get('622db5ecf978a3e718b61933')
        self.assertIsNone(user_data)

    async def test_create_with_same_email(self):
        await self.crud.create({'name': 'pushkin', 'email': 'pushkin@mail.com', 'password': 'veverbi344'})
        with self.assertRaises(UniqueIndexException) as e:
            await self.crud.create({'name': 'evgestrogan', 'email': 'pushkin@mail.com', 'password': 'ybuhvdfjv34r2'})
            self.assertIsInstance(e, UniqueIndexException)

    async def test_get_all_users(self):
        await self.crud.create({'name': 'pushkin', 'email': 'pushkin@mail.com', 'password': 'veverbi344'})
        await self.crud.create({'name': 'evgestrogan', 'email': 'evgestrogan@mail.com', 'password': 'btrbt345'})
        await self.crud.create({'name': 'nikolay', 'email': 'nikolay@mail.com', 'password': 'grbwvr4315btr'})
        users = await self.crud.get_all()
        self.assertIsInstance(users, list)
        self.assertEqual(3, len(users))

    async def test_remove_user(self):
        await self.crud.create({'name': 'pushkin', 'email': 'pushkin@mail.com', 'password': 'veverbi344'})
        user = await self.crud.create({'name': 'evgestrogan', 'email': 'evgestrogan@mail.com', 'password': 'btrbt345'})
        result = await self.crud.delete(user)
        users = await self.crud.get_all()
        self.assertEqual(1, len(users))
        self.assertEqual(result, 1)

    async def test_remove_user_with_wrong_id(self):
        result = await self.crud.delete('2437328459ettbfe')
        self.assertIsNone(result)

    async def test_remove_not_exist_user(self):
        result = await self.crud.delete('622db5ecf978a3e718b61934')
        self.assertIsNone(result)



