from fastapi import HTTPException
from starlette import status
from starlette.requests import Request


async def must_authentication(request: Request):
    if request.scope['user'] is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return request.scope['user']


