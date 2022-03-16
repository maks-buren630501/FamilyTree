from starlette.requests import Request
from fastapi.responses import JSONResponse


async def error_handler_middleware(request: Request, call_next):
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
            return JSONResponse(e.args, status_code=423)
        except:
            return JSONResponse({'detail': 'error description is not json serialised'}, status_code=423)


