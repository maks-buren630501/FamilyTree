from enum import Enum
from typing import List

from fastapi import status

from backend.authentication.schemas import UserSchemaGet
from backend.core.additional import BaseUrlConfig


class ResponseDescription(Enum):
    CONFLICT: Enum = {
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
    NO_CONTENT: Enum = {
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
    description='Обновить данные о пользователе в системе',
    responses={
        status.HTTP_409_CONFLICT: ResponseDescription.CONFLICT.value,
        status.HTTP_204_NO_CONTENT: ResponseDescription.NO_CONTENT.value
    },
    response_model=str,
    status_code=status.HTTP_201_CREATED
)

delete_user_url_config = AuthenticationUrlConfig(
    tags=['user'],
    name='Удаление пользователя',
    description='Удалить пользователя из системые',
    responses={
        status.HTTP_204_NO_CONTENT: ResponseDescription.NO_CONTENT.value
    },
    response_model=str,
    status_code=status.HTTP_200_OK
)

registration_user_url_config = AuthenticationUrlConfig(
    tags=['user'],
    name='Регистрация пользователя',
    description='Регистрация пользователя в системе, необходима активация',
    responses={
        status.HTTP_409_CONFLICT: ResponseDescription.CONFLICT.value
    },
    response_model=str,
    status_code=status.HTTP_201_CREATED
)

activate_user_url_config = AuthenticationUrlConfig(
    tags=['user'],
    name='Активация аккаунта пользователя',
    description='Активация аккаунта пользователя в системе',
    responses={
        status.HTTP_204_NO_CONTENT: ResponseDescription.NO_CONTENT.value
    },
    response_model=str,
    status_code=status.HTTP_201_CREATED
)

login_user_url_config = AuthenticationUrlConfig(
    tags=['user'],
    name='Логин пользователя',
    description='Вход пользователя в систему',
    responses={
        status.HTTP_403_FORBIDDEN: ResponseDescription.NO_CONTENT.value
    },
    response_model=str,
    status_code=status.HTTP_200_OK
)

logout_user_url_config = AuthenticationUrlConfig(
    tags=['user'],
    name='Выход пользователя',
    description='Выход пользователя из системы',
    responses={
        status.HTTP_403_FORBIDDEN: ResponseDescription.NO_CONTENT.value
    },
    response_model=str,
    status_code=status.HTTP_200_OK
)

refresh_url_config = AuthenticationUrlConfig(
    tags=['user'],
    name='Обновление токена',
    description='Обновление токена пользователя',
    responses={
        status.HTTP_403_FORBIDDEN: ResponseDescription.NO_CONTENT.value
    },
    response_model=str,
    status_code=status.HTTP_200_OK
)
