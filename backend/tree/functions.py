import uuid
from typing import List

from core.database.crud import Crud
from core.exception.base_exeption import NoDataException
from tree.models import PartnersMapper, PartnersGet, NodeSchemaGet
from tree.queries import get_select_node_with_users_query


def get_partner(partner: PartnersMapper, other_id: str):
    return PartnersGet(id=partner.id, partner_id=partner.husband_id if partner.wife_id == other_id else partner.wife_id,
                       wedding_date=partner.wedding_date, divorce_date=partner.divorce_date)


def get_nodes_from_query_result(nodes_with_partners: list) -> List[NodeSchemaGet]:
    nodes = {}
    for item in nodes_with_partners:
        partner = get_partner(item[1], item[0].id) if item[1] else None
        if nodes.get(item[0].id) is None:
            nodes[item[0].id] = NodeSchemaGet(**item[0].__dict__, partners=[partner] if partner else [])
        else:
            if partner:
                nodes[item[0].id].partners.append(partner)
    return list(nodes.values())


async def check_permission_to_nodes(user_id: uuid.UUID, node_ids: List[uuid.UUID]):
    nodes_data = [await Crud.get_all(get_select_node_with_users_query(str(node_id))) for node_id in node_ids]
    if all([len(item) > 0 for item in nodes_data]):
        nodes = [node_data[0][0] for node_data in nodes_data]
        author_user_ids = [[node.author_id, node.user_id] for node in nodes]
        user_ids = [[item[1].user_id for item in node_data if item[1]] for node_data in nodes_data]
        if user_id in set([item for sublist in user_ids + author_user_ids for item in sublist if item]):
            return True
        else:
            return False
    else:
        raise NoDataException('One foreign key is no correct')



