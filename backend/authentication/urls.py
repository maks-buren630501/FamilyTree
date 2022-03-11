from typing import List

from fastapi import FastAPI, Response, status
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

from backend.authentication.config import get_users_url_config, get_user_url_config, create_user_url_config, \
    update_user_url_config
from backend.authentication.crud import UserCrud
from backend.authentication.schemas import UserSchemaGet, UserSchemaCreate, PyObjectId, UpdateUserSchema
from backend.core.exception.base_exeption import UniqueIndexException, ObjectNotExistException
from backend.core.exception.http_exeption import NotUniqueIndex, ObjectNotExist
from backend.core.middleware import error_handler_middleware

app_authentication = FastAPI(middleware=[Middleware(BaseHTTPMiddleware, dispatch=error_handler_middleware)])


@app_authentication.get('/{user_id}', **get_user_url_config.dict())
async def get_user(user_id: PyObjectId) -> UserSchemaGet | Response:
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
async def update_user(user_id: PyObjectId, user: UpdateUserSchema) -> int:
    user = {k: v for k, v in user.dict().items() if v is not None}
    try:
        return await UserCrud.update(user_id, user)
    except UniqueIndexException as e:
        raise NotUniqueIndex(e)
    except ObjectNotExistException as e:
        raise ObjectNotExist(e)
