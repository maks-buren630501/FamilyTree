import uuid
from typing import List

from fastapi import FastAPI
from sqlmodel import select, or_
from starlette import status
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from core.database.crud import Crud
from core.decorators import must_authentication
from core.exception.base_exeption import UniqueIndexException, ForeignKeyErrorException
from core.exception.http_exeption import NotUniqueIndex, ForeignKeyError
from core.middleware import error_handler_middleware
from tree.config import get_node_url_config, create_node_url_config, get_nodes_url_config, update_node_url_config, \
    create_partner_url_config
from tree.functions import get_partner
from tree.models import BaseNodeSchema, NodeDataBase, UserNodeMapper, PartnersMapper, BasePartners, NodeSchemaGet, \
    NodeSchemaUpdate

app_tree = FastAPI(middleware=[Middleware(BaseHTTPMiddleware, dispatch=error_handler_middleware)])


@app_tree.get('/{node_id}', **get_node_url_config.dict(), response_model_exclude_unset=True)
@must_authentication
async def get_node(request: Request, node_id: str) -> NodeSchemaGet | Response:
    user_id = uuid.UUID(request.scope['user'])
    result = await Crud.get_all(select(NodeDataBase, UserNodeMapper, PartnersMapper).
                                join(UserNodeMapper, isouter=True).
                                join(PartnersMapper,
                                     or_(PartnersMapper.husband_id == NodeDataBase.id,
                                         PartnersMapper.wife_id == NodeDataBase.id),
                                     isouter=True).
                                where(NodeDataBase.id == node_id))
    if len(result) > 0:
        node: NodeDataBase = result[0][0]
        partners = [get_partner(item[2], node_id) for item in result if item[2]]
        if user_id in [item[1].user_id for item in result if item[1]] + [node.author_id, node.user_id]:
            return NodeSchemaGet(**node.__dict__, partners=partners)
        else:
            Response(status_code=status.HTTP_403_FORBIDDEN)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app_tree.get('/', **get_nodes_url_config.dict(), response_model_exclude_unset=True)
@must_authentication
async def get_nodes(request: Request) -> List[NodeSchemaGet]:
    user_id = request.scope['user']
    result = await Crud.get_all(select(NodeDataBase, PartnersMapper).join(UserNodeMapper, isouter=True).
                                join(PartnersMapper,
                                     or_(PartnersMapper.husband_id == NodeDataBase.id,
                                         PartnersMapper.wife_id == NodeDataBase.id),
                                     isouter=True).
                                where(or_(UserNodeMapper.user_id == user_id,
                                          NodeDataBase.user_id == user_id,
                                          NodeDataBase.author_id == user_id)))
    nodes = {}
    for item in result:
        partner = get_partner(item[1], item[0].id)
        if nodes.get(item[0].id) is None:
            nodes[item[0].id] = NodeSchemaGet(**item[0].__dict__, partners=[partner])
        else:
            nodes[item[0].id].partners.append(partner)
    return list(nodes.values())


@app_tree.post('/', **create_node_url_config.dict())
@must_authentication
async def create_node(request: Request, node: BaseNodeSchema) -> uuid.UUID | Response:
    author_id = request.scope['user']
    try:
        new_node = await Crud.save(NodeDataBase(**node.__dict__, author_id=author_id))
    except UniqueIndexException as e:
        raise NotUniqueIndex(e)
    except ForeignKeyErrorException as e:
        raise ForeignKeyError(e)
    else:
        return new_node


@app_tree.put('/{node_id}', **update_node_url_config.dict())
@must_authentication
async def update_node(request: Request, node_id: str, node_update: NodeSchemaUpdate) -> uuid.UUID | Response:
    user_id = uuid.UUID(request.scope['user'])
    result = await Crud.get_all(select(NodeDataBase, UserNodeMapper).
                                join(UserNodeMapper, isouter=True).
                                where(NodeDataBase.id == node_id))
    if len(result) > 0:
        node: NodeDataBase = result[0][0]
        if user_id in [item[1].user_id for item in result if item[1]] + [node.author_id, node.user_id]:
            data_to_update = node_update.dict(exclude_unset=True)
            for key, value in data_to_update.items():
                setattr(node, key, value)
            try:
                return await Crud.save(node)
            except UniqueIndexException as e:
                raise NotUniqueIndex(e)
            except ForeignKeyErrorException as e:
                raise ForeignKeyError(e)
        else:
            Response(status_code=status.HTTP_403_FORBIDDEN)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app_tree.post('/partner', **create_partner_url_config.dict())
@must_authentication
async def create_partner(partner_mapper: BasePartners) -> uuid.UUID | Response:
    try:
        new_partners = await Crud.save(PartnersMapper(**partner_mapper.__dict__))
    except ForeignKeyErrorException as e:
        raise ForeignKeyError(e)
    else:
        return new_partners
