import datetime
from typing import List
from unittest import IsolatedAsyncioTestCase

from sqlmodel import select, or_

from core.database.crud import Crud
from core.database.migrations import clear_tables
from tree.models import NodeDataBase, UserNodeMapper, PartnersMapper
from user.models import UserDataBase


class UserCrudTestCase(IsolatedAsyncioTestCase):

    async def asyncTearDown(self):
        await clear_tables()

    async def test_get_node(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        node = await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user))
        node_data_base: NodeDataBase = await Crud.get(select(NodeDataBase).where(NodeDataBase.id == node))
        self.assertEqual(node_data_base.name, 'Andrey')
        self.assertEqual(node_data_base.family_name, 'Bichkoy')
        self.assertEqual(node_data_base.author_id, user)

    async def test_get_not_exist_node(self):
        node_data_base: NodeDataBase = await Crud.get(select(NodeDataBase).
                                                      where(NodeDataBase.id == '9eaa13a1-120f-4f5c-8461-ee4530b2c37e'))
        self.assertIsNone(node_data_base)

    async def test_get_nodes(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user))
        await Crud.save(NodeDataBase(name='Sergei', family_name='Trifonov', author_id=user))
        nodes: List[NodeDataBase] = await Crud.get_all(select(NodeDataBase))
        self.assertEqual(len(nodes), 2)

    async def test_get_nodes_with_partners(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        node_1 = await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user))
        node_2 = await Crud.save(NodeDataBase(name='Elena', family_name='Trifonova', author_id=user))
        await Crud.save(PartnersMapper(husband_id=node_1, wife_id=node_2, wedding_date=datetime.date(2000, 1, 1)))
        result = await Crud.get_all(select(NodeDataBase, PartnersMapper).
                                    join(PartnersMapper,
                                         or_(
                                             PartnersMapper.husband_id == NodeDataBase.id,
                                             PartnersMapper.wife_id == NodeDataBase.id
                                         ),
                                    isouter=True))
        self.assertEqual(len(result), 2)
        for item in result:
            self.assertEqual(item[1].wedding_date, datetime.date(2000, 1, 1))

    async def test_get_nodes_with_users(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        user_2 = await Crud.save(UserDataBase(username='zero', password=b'veverbi344', email='zero@mail.com'))
        user_3 = await Crud.save(UserDataBase(username='evgen', password=b'veverbi344', email='evgen@mail.com'))
        node_1 = await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user))
        node_2 = await Crud.save(NodeDataBase(name='Elena', family_name='Trifonova', author_id=user))
        await Crud.save(UserNodeMapper(node_id=node_1, user_id=user_2))
        await Crud.save(UserNodeMapper(node_id=node_2, user_id=user_2))
        await Crud.save(UserNodeMapper(node_id=node_2, user_id=user_3))
        result = await Crud.get_all(select(NodeDataBase, UserNodeMapper).
                                    join(UserNodeMapper, isouter=True))
        self.assertEqual(len(result), 3)
        for item in result:
            self.assertIs(type(item[1]), UserNodeMapper)

    async def test_delete_node(self):
        user = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        node_id = await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user))
        node = await Crud.get(select(NodeDataBase).where(NodeDataBase.id == node_id))
        await Crud.delete(node)
        nodes: List[NodeDataBase] = await Crud.get_all(select(NodeDataBase))
        self.assertEqual(len(nodes), 0)

    async def test_delete_author_node(self):
        user_id = await Crud.save(UserDataBase(username='pushkin', password=b'veverbi344', email='pushkin@mail.com'))
        await Crud.save(NodeDataBase(name='Andrey', family_name='Bichkoy', author_id=user_id))
        user = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
        await Crud.delete(user)
        nodes: List[NodeDataBase] = await Crud.get_all(select(NodeDataBase))
        self.assertEqual(len(nodes), 0)





