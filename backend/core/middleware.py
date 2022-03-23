import traceback
import uuid

from jose import JWTError
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from backend.core.additional import decode_token
from backend.core.logger import log_request, log_error


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
        log_error(request.scope['request_id'], traceback.format_exc())
        try:
            return Response(e.args[0], status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
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


async def log_middleware(request: Request, call_next) -> Response:
    user = request.scope['user']
    client_address = request.client.host
    client_port = request.client.port
    method = request.method
    url = request.url
    request_id = uuid.uuid4()
    request.scope['request_id'] = request_id
    response = await call_next(request)
    response_status = response.status_code
    log_request(request_id, method, url, client_address, client_port, user, response_status)
    return response


