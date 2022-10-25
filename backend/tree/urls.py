import uuid
from typing import List

from fastapi import FastAPI, Depends
from starlette import status
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from core.database.crud import Crud
from core.dependencies import must_authentication
from core.exception.base_exeption import UniqueIndexException, ForeignKeyErrorException
from core.exception.http_exeption import NotUniqueIndex, ForeignKeyError
from core.middleware import error_handler_middleware
from tree.config import get_node_url_config, create_node_url_config, get_nodes_url_config, update_node_url_config, \
    create_partner_url_config, delete_node_url_config, search_nodes_url_config, find_nodes_url_config, \
    get_children_url_config
from tree.functions import get_partner, get_nodes_from_query_result
from tree.models import BaseNodeSchema, NodeDataBase, PartnersMapper, BasePartners, NodeSchemaGet, \
    NodeSchemaUpdate
from tree.queries import get_select_node_with_partners_query, get_select_node_with_users_query,\
    get_search_nodes_with_partners_query, get_find_nodes_with_partners_query, get_select_children_with_partners_query,\
    get_select_nodes_with_partners_query_by_user


app_tree = FastAPI(middleware=[Middleware(BaseHTTPMiddleware, dispatch=error_handler_middleware)])


@app_tree.get('/{node_id}', **get_node_url_config.dict(), response_model_exclude_unset=True)
async def get_node(node_id: str) -> NodeSchemaGet | Response:
    result = await Crud.get_all(get_select_node_with_partners_query(node_id))
    if len(result) > 0:
        node: NodeDataBase = result[0][0]
        partners = [get_partner(item[1], node_id) for item in result if item[1]]
        return NodeSchemaGet(**node.__dict__, partners=partners)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app_tree.get('/', **get_nodes_url_config.dict())
async def get_nodes(user_id: str = Depends(must_authentication)) -> List[NodeSchemaGet]:
    result = await Crud.get_all(get_select_nodes_with_partners_query_by_user(user_id))
    return get_nodes_from_query_result(result)


@app_tree.get('/children/{node_id}', **get_children_url_config.dict(), response_model_exclude_unset=True)
async def get_children(node_id: str) -> List[NodeSchemaGet]:
    result = await Crud.get_all(get_select_children_with_partners_query(node_id))
    return get_nodes_from_query_result(result)


@app_tree.get('/search/{query}', **search_nodes_url_config.dict(), response_model_exclude_unset=True)
async def search_nodes(query: str) -> List[NodeSchemaGet]:
    result = await Crud.get_all(get_search_nodes_with_partners_query(query))
    return get_nodes_from_query_result(result)


@app_tree.post('/find', **find_nodes_url_config.dict(), response_model_exclude_unset=True)
async def find_nodes(node: NodeSchemaUpdate) -> List[NodeSchemaGet]:
    result = await Crud.get_all(get_find_nodes_with_partners_query(node))
    return get_nodes_from_query_result(result)


@app_tree.post('/', **create_node_url_config.dict())
async def create_node(node: BaseNodeSchema, user_id: str = Depends(must_authentication)) -> uuid.UUID | Response:
    try:
        new_node = await Crud.save(NodeDataBase(**node.__dict__, author_id=user_id))
    except UniqueIndexException as e:
        raise NotUniqueIndex(e)
    except ForeignKeyErrorException as e:
        raise ForeignKeyError(e)
    else:
        return new_node


@app_tree.put('/{node_id}', **update_node_url_config.dict())
async def update_node(node_id: str, node_update: NodeSchemaUpdate, user_id: str = Depends(must_authentication)) -> uuid.UUID | Response:
    result = await Crud.get_all(get_select_node_with_users_query(node_id))
    if len(result) > 0:
        node: NodeDataBase = result[0][0]
        if uuid.UUID(user_id) in [item[1].user_id for item in result if item[1]] + [node.author_id, node.user_id]:
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
            return Response(status_code=status.HTTP_403_FORBIDDEN)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app_tree.delete('/{node_id}', **delete_node_url_config.dict())
async def delete_node(node_id: str, user_id: str = Depends(must_authentication)) -> Response:
    result = await Crud.get_all(get_select_node_with_users_query(node_id))
    if len(result) > 0:
        node: NodeDataBase = result[0][0]
        if uuid.UUID(user_id) in [item[1].user_id for item in result if item[1]] + [node.author_id, node.user_id]:
            await Crud.delete(node)
            return Response(status_code=status.HTTP_200_OK)
        else:
            return Response(status_code=status.HTTP_403_FORBIDDEN)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app_tree.post('/partner', **create_partner_url_config.dict(), dependencies=[Depends(must_authentication)])
async def create_partner(partner_mapper: BasePartners) -> uuid.UUID | Response:
    try:
        return await Crud.save(PartnersMapper(**partner_mapper.__dict__))
    except ForeignKeyErrorException as e:
        raise ForeignKeyError(e)

