from unittest import IsolatedAsyncioTestCase

from core.exception.base_exeption import UniqueIndexException


class UserCrudTestCase(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        init_database_client()
        self.connection = get_database()
        self.crud = UserCrud()

    async def asyncTearDown(self):
        await self.connection.database.get_collection("users").delete_many({})
        self.connection.client.close()

    async def test_get_user_by_id(self):
        user = await self.crud.create({'username': 'pushkin', 'email': 'pushkin@mail.com', 'password': b'veverbi344'})
        user_data = await self.crud.get(user)
        self.assertEqual(user_data['username'], 'pushkin')
        self.assertEqual(user_data['email'], 'pushkin@mail.com')
        self.assertEqual(user_data['password'], b'veverbi344')

    async def test_get_user_by_wroregistrationng_id(self):
        user_data = await self.crud.get('2437328459ettb')
        self.assertIsNone(user_data)

    async def test_get_not_exist_user(self):
        user_data = await self.crud.get('622db5ecf978a3e718b61933')
        self.assertIsNone(user_data)

    async def test_create_with_same_email(self):
        await self.crud.create({'username': 'pushkin', 'email': 'pushkin@mail.com', 'password': b'veverbi344'})
        with self.assertRaises(UniqueIndexException) as e:
            await self.crud.create({'username': 'evgestrogan', 'email': 'pushkin@mail.com', 'password': b'ybuhvdfjv34r2'})
            self.assertIsInstance(e, UniqueIndexException)

    async def test_get_all_users(self):
        await self.crud.create({'username': 'pushkin', 'email': 'pushkin@mail.com', 'password': b'veverbi344'})
        await self.crud.create({'username': 'evgestrogan', 'email': 'evgestrogan@mail.com', 'password': b'btrbt345'})
        await self.crud.create({'username': 'nikolay', 'email': 'nikolay@mail.com', 'password': b'grbwvr4315btr'})
        users = await self.crud.get_all()
        self.assertIsInstance(users, list)
        self.assertEqual(3, len(users))

    async def test_remove_user(self):
        await self.crud.create({'username': 'pushkin', 'email': 'pushkin@mail.com', 'password': b'veverbi344'})
        user = await self.crud.create({'username': 'evgestrogan', 'email': 'evgestrogan@mail.com', 'password': b'btrbt345'})
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

    async def test_find_user(self):
        await self.crud.create({'username': 'pushkin', 'email': 'pushkin@mail.com', 'password': b'veverbi344'})
        await self.crud.create({'username': 'anton', 'email': 'anton@mail.com', 'password': b'rb43q4gbtrb3'})
        find_user = await self.crud.find({'username': 'anton'})
        self.assertEqual('anton@mail.com', find_user['email'])

    async def test_find_not_exist_user(self):
        await self.crud.create({'username': 'pushkin', 'email': 'pushkin@mail.com', 'password': b'veverbi344'})
        find_user = await self.crud.find({'username': 'anton'})
        self.assertIsNone(find_user)




