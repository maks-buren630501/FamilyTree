from typing import List

from fastapi import status

from core.config import ResponseDescription
from user.schemas import UserSchemaGet
from core.additional import BaseUrlConfig


class UserUrlConfig(BaseUrlConfig):
    responses: dict | None


get_user_url_config = UserUrlConfig(
    tags=['user'],
    name='Пользователь',
    description='Получить пользователя по его ID',
    responses={
        status.HTTP_204_NO_CONTENT: ResponseDescription.NO_CONTENT.value
    },
    response_model=UserSchemaGet,
    status_code=status.HTTP_200_OK
)

get_users_url_config = UserUrlConfig(
    tags=['user'],
    name='Список пользователей',
    description='Получить всех пользователей зарегестрированных в системе',
    response_model=List[UserSchemaGet],
    status_code=status.HTTP_200_OK
)

create_user_url_config = UserUrlConfig(
    tags=['user'],
    name='Создать пользователя',
    description='Зарегестрировать пользователя в системе',
    responses={
        status.HTTP_409_CONFLICT: ResponseDescription.CONFLICT.value,
        status.HTTP_406_NOT_ACCEPTABLE: ResponseDescription.CONFLICT.value
    },
    response_model=str,
    status_code=status.HTTP_201_CREATED
)

update_user_url_config = UserUrlConfig(
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

delete_user_url_config = UserUrlConfig(
    tags=['user'],
    name='Удаление пользователя',
    description='Удалить пользователя из системые',
    responses={
        status.HTTP_204_NO_CONTENT: ResponseDescription.NO_CONTENT.value
    },
    response_model=str,
    status_code=status.HTTP_200_OK
)

registration_user_url_config = UserUrlConfig(
    tags=['user'],
    name='Регистрация пользователя',
    description='Регистрация пользователя в системе, необходима активация',
    responses={
        status.HTTP_409_CONFLICT: ResponseDescription.CONFLICT.value
    },
    response_model=str,
    status_code=status.HTTP_201_CREATED
)


