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
from core.exception.base_exeption import UniqueIndexException
from core.exception.http_exeption import NotUniqueIndex
from core.middleware import error_handler_middleware
from tree.config import get_node_url_config, create_node_url_config, get_nodes_url_config
from tree.models import BaseNodeSchema, NodeDataBase, UserNodeMapper

app_tree = FastAPI(middleware=[Middleware(BaseHTTPMiddleware, dispatch=error_handler_middleware)])


@app_tree.get('/{node_id}', **get_node_url_config.dict(), response_model_exclude_unset=True)
@must_authentication
async def get_node(request: Request, node_id: str) -> BaseNodeSchema | Response:
    user_id = uuid.UUID(request.scope['user'])
    node_with_links = await Crud.get_all(select(NodeDataBase, UserNodeMapper).join(UserNodeMapper, isouter=True).
                                         where(NodeDataBase.id == node_id))
    if len(node_with_links) > 0:
        node: NodeDataBase = node_with_links[0][0]
        if user_id in [item[1].user_id for item in node_with_links if item[1]] + [node.author_id, node.user_id]:
            return node
        else:
            Response(status_code=status.HTTP_403_FORBIDDEN)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app_tree.get('/', **get_nodes_url_config.dict(), response_model_exclude_unset=True)
@must_authentication
async def get_nodes(request: Request) -> List[BaseNodeSchema]:
    user_id = request.scope['user']
    nodes = await Crud.get_all(select(NodeDataBase).join(UserNodeMapper, isouter=True).
                               where(or_(UserNodeMapper.user_id == user_id,
                                         NodeDataBase.user_id == user_id,
                                         NodeDataBase.author_id == user_id)))
    return nodes


@app_tree.post('/', **create_node_url_config.dict())
@must_authentication
async def create_node(request: Request, node: BaseNodeSchema) -> uuid.UUID | Response:
    author_id = request.scope['user']
    try:
        new_node = await Crud.save(NodeDataBase(**node.params, author_id=author_id))
    except UniqueIndexException as e:
        raise NotUniqueIndex(e)
    else:
        return new_node
