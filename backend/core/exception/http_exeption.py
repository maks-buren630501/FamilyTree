from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

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
