from fastapi import FastAPI, Depends
from starlette import status
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from backend.core.exception.base_exeption import UniqueIndexException
from backend.core.exception.http_exeption import NotUniqueIndex
from backend.core.middleware import error_handler_middleware
from backend.tree.config import get_node_url_config, create_node_url_config, update_node_url_config, \
    delete_node_url_config
from backend.tree.crud import NodeCrud
from backend.tree.dependence import node_crud
from backend.tree.schemas import NodeSchemaGet, BaseNodeSchema, UpdateNodeSchema

app_tree = FastAPI(middleware=[Middleware(BaseHTTPMiddleware, dispatch=error_handler_middleware)])


@app_tree.get('/{node_id}', **get_node_url_config.dict(), response_model_exclude_unset=True)
async def get_node(node_id: str, crud: NodeCrud = Depends(node_crud)) -> NodeSchemaGet | Response:
    node = await crud.get(node_id)
    if node:
        return NodeSchemaGet(**node)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app_tree.post('/', **create_node_url_config.dict())
async def create_node(request: Request, node: BaseNodeSchema, crud: NodeCrud = Depends(node_crud)) -> str | Response:
    try:
        if not request.scope['user']:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        node.author_id = request.scope['user']
        node = {k: v for k, v in node.dict().items() if v is not None}
        new_node = await crud.create(node)
        return new_node
    except UniqueIndexException as e:
        raise NotUniqueIndex(e)


@app_tree.put('/{node_id}', **update_node_url_config.dict())
async def update_node(request: Request, node_id: str, node: UpdateNodeSchema, crud: NodeCrud = Depends(node_crud)) -> int | Response:
    try:
        if not request.scope['user']:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        database_node = await crud.get(node_id)
        if not database_node:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        if database_node['author_id'] != request.scope['user']:
            return Response(status_code=status.HTTP_403_FORBIDDEN)
        node = {k: v for k, v in node.dict().items() if v is not None}
        update_count = await crud.update(node_id, node)
        if update_count:
            return update_count
        else:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    except UniqueIndexException as e:
        raise NotUniqueIndex(e)


@app_tree.delete('/{node_id}', **delete_node_url_config.dict())
async def delete_node(request: Request, node_id: str, crud: NodeCrud = Depends(node_crud)) -> int | Response:
    if not request.scope['user']:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    database_node = await crud.get(node_id)
    if not database_node:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    if database_node['author_id'] != request.scope['user']:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    delete_count = await crud.delete(node_id)
    if delete_count:
        return delete_count
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
