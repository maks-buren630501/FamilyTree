from enum import Enum
from typing import List

from fastapi import status

from backend.authentication.schemas import UserSchemaGet
from backend.core.additional import BaseUrlConfig


class ResponseDescription(Enum):
    CONFLICT: dict = {
        "description": "Ошибка проверки уникальности значений",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                          "loc": [
                            "string"
                          ],
                          "msg": "string",
                          "type": "string"
                        }
                      ]
                }
            }
        }
    }
    NO_CONTENT: dict = {
        "description": "Пустой ответ"
    }


class AuthenticationUrlConfig(BaseUrlConfig):
    responses: dict | None


get_user_url_config = AuthenticationUrlConfig(
    tags=['user'],
    name='Пользователь',
    description='Получить пользователя по его ID',
    responses={
        status.HTTP_204_NO_CONTENT: ResponseDescription.NO_CONTENT.value
    },
    response_model=UserSchemaGet,
    status_code=status.HTTP_200_OK
)

get_users_url_config = AuthenticationUrlConfig(
    tags=['user'],
    name='Список пользователей',
    description='Получить всех пользователей зарегестрированных в системе',
    response_model=List[UserSchemaGet],
    status_code=status.HTTP_200_OK
)

create_user_url_config = AuthenticationUrlConfig(
    tags=['user'],
    name='Создать пользователя',
    description='Зарегестрировать пользователя в системе',
    responses={
        status.HTTP_409_CONFLICT: ResponseDescription.CONFLICT.value
    },
    response_model=str,
    status_code=status.HTTP_201_CREATED
)

update_user_url_config = AuthenticationUrlConfig(
    tags=['user'],
    name='Обновление пользователя',
    description='Оновить данные о пользователе в системе',
    responses={
        status.HTTP_409_CONFLICT: ResponseDescription.CONFLICT.value,
        status.HTTP_204_NO_CONTENT: ResponseDescription.NO_CONTENT.value
    },
    response_model=str,
    status_code=status.HTTP_201_CREATED
)
