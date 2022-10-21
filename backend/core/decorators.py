from functools import wraps

from fastapi import HTTPException
from starlette import status
from starlette.requests import Request


def must_authentication(func):

    @wraps(func)
    async def wrap(request: Request, *args, **kwargs):
        if request.scope['user'] is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        else:
            return await func(request, *args, **kwargs)

    return wrap
