from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from jose import JWTError

from backend.core.exception.base_exeption import UniqueIndexException


def create_message(loc: list, msg: str, type_exc: str) -> str:
    return jsonable_encoder(
        {
            "loc": loc,
            "msg": msg,
            "type": type_exc
        }
    )


class NotUniqueIndex(HTTPException):
    """Обработчик ошибки занесения уникального значения."""

    def __init__(self, exc: UniqueIndexException):
        loc = ['body', list(exc.detail['keyPattern'].keys())[0]]
        msg, type_exc, *_ = exc.detail['errmsg'].split(': ')
        self.status_code = status.HTTP_409_CONFLICT
        super().__init__(detail=create_message(loc, msg, type_exc), status_code=self.status_code)


class TokenError(HTTPException):
    """Обработчик ошибки занесения уникального значения."""

    def __init__(self, exc: JWTError):
        jwt_error = str(exc)
        if jwt_error == 'Not enough segments':
            self.message = 'Incorrect token structure'
            self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        elif jwt_error == 'Signature has expired.':
            self.message = 'token time is out'
            self.status_code = status.HTTP_408_REQUEST_TIMEOUT
        else:
            self.message = 'unknow token error'
            self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        super().__init__(detail={'message': self.message}, status_code=self.status_code)
