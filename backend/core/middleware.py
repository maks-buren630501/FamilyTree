from jose import JWTError
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

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
    access_token = request.headers.get('x-access-token')
    if access_token:
        try:
            user_data = decode_token(access_token)
            request.scope['user'] = user_data.get('user_id')
        except JWTError:
            request.scope['user'] = None
    else:
        request.scope['user'] = None
    response = await call_next(request)
    return response
