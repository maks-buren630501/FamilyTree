from jose import JWTError
from starlette import status
from starlette.requests import Request
from fastapi.responses import JSONResponse
from starlette.responses import Response

from backend.authentication.functions import update_refresh_token
from backend.core.additional import decode_token


async def error_handler_middleware(request: Request, call_next) -> Response:
    """
    Функция для обработки остаточных ошибок
    :param request: http запрос
    :param call_next: функция обработки запроса
    :return: результат выполнения запроса либо json ответ с текстом ошибки и кодом 422
    """
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        try:
            return Response(e.args, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except TypeError:
            return Response('Error description is not json serialised', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            return Response('Unknown error', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def authentication_middleware(request: Request, call_next) -> Response:
    new_access_token = None
    access_token = request.cookies.get('access_token')
    try:
        user_data = decode_token(access_token)
    except (JWTError, AttributeError):
        refresh_token = request.cookies.get('refresh_token')
        if refresh_token:
            new_access_token = await update_refresh_token(refresh_token)
            if new_access_token:
                user_data = decode_token(new_access_token)
            else:
                user_data = {}
        else:
            user_data = {}
    request.scope['user'] = user_data.get('user_id')
    response = await call_next(request)
    if new_access_token:
        response.set_cookie(key='access_token', value=new_access_token, httponly=True, path='api/')
    return response
