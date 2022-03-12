from typing import List

from fastapi import FastAPI, Response, status
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

from backend.authentication.config import get_users_url_config, get_user_url_config, create_user_url_config, \
    update_user_url_config, delete_user_url_config
from backend.authentication.crud import UserCrud
from backend.authentication.schemas import UserSchemaGet, UserSchemaCreate, UpdateUserSchema
from backend.core.exception.base_exeption import UniqueIndexException
from backend.core.exception.http_exeption import NotUniqueIndex
from backend.core.middleware import error_handler_middleware

app_authentication = FastAPI(middleware=[Middleware(BaseHTTPMiddleware, dispatch=error_handler_middleware)])


@app_authentication.get('/{user_id}', **get_user_url_config.dict())
async def get_user(user_id: str) -> UserSchemaGet | Response:
    user = await UserCrud.get(user_id)
    if user:
        return UserSchemaGet(**user)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app_authentication.get('/', **get_users_url_config.dict())
async def get_users() -> List[UserSchemaGet]:
    users = await UserCrud.get_all()
    return [UserSchemaGet(**user) for user in users]


@app_authentication.post('/', **create_user_url_config.dict())
async def create_user(user: UserSchemaCreate) -> str:
    try:
        user = await UserCrud.create(user.dict())
        return user
    except UniqueIndexException as e:
        raise NotUniqueIndex(e)


@app_authentication.put('/{user_id}', **update_user_url_config.dict())
async def update_user(user_id: str, user: UpdateUserSchema) -> int | Response:
    user = {k: v for k, v in user.dict().items() if v is not None}  # Удаление ключей со значением Null
    try:
        update_count = await UserCrud.update(user_id, user)
        if update_count:
            return update_count
        else:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    except UniqueIndexException as e:
        raise NotUniqueIndex(e)


@app_authentication.delete('/{user_id}', **delete_user_url_config.dict())
async def delete_user(user_id: str) -> int | Response:
    delete_count = await UserCrud.delete(user_id)
    if delete_count:
        return delete_count
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
