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
            return JSONResponse(e.args, status_code=500)
        except TypeError:
            return JSONResponse({'detail': 'Error description is not json serialised'}, status_code=500)
        except:
            return JSONResponse({'detail': 'Unknow error'}, status_code=500)

