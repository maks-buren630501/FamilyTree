from fastapi import status

from backend.core.additional import BaseUrlConfig
from backend.core.config import ResponseDescription


class AuthenticationUrlConfig(BaseUrlConfig):
    responses: dict | None


registration_url_config = AuthenticationUrlConfig(
    tags=['user'],
    name='Регистрация пользователя',
    description='Регистрация пользователя в системе, необходима активация',
    responses={
        status.HTTP_409_CONFLICT: ResponseDescription.CONFLICT.value
    },
    response_model=str,
    status_code=status.HTTP_201_CREATED
)

activate_url_config = AuthenticationUrlConfig(
    tags=['user'],
    name='Активация аккаунта пользователя',
    description='Активация аккаунта пользователя в системе',
    responses={
        status.HTTP_204_NO_CONTENT: ResponseDescription.NO_CONTENT.value
    },
    response_model=str,
    status_code=status.HTTP_201_CREATED
)

login_url_config = AuthenticationUrlConfig(
    tags=['user'],
    name='Логин пользователя',
    description='Вход пользователя в систему',
    responses={
        status.HTTP_403_FORBIDDEN: ResponseDescription.NO_CONTENT.value
    },
    response_model=dict,
    status_code=status.HTTP_200_OK
)

logout_url_config = AuthenticationUrlConfig(
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
    response_model=dict,
    status_code=status.HTTP_200_OK
)

start_recovery_password_url_config = AuthenticationUrlConfig(
    tags=['user'],
    name='Запрос на восстановление парроля',
    description='Запрос на восстановление парроля',
    responses={
        status.HTTP_404_NOT_FOUND: ResponseDescription.NO_CONTENT.value
    },
    response_model=dict,
    status_code=status.HTTP_200_OK
)

check_recovery_password_url_config = AuthenticationUrlConfig(
    tags=['user'],
    name='Проверка - восстанавливает ли данный пользователь пароль',
    description='Проверка - восстанавливает ли данный пользователь пароль',
    responses={
        status.HTTP_403_FORBIDDEN: ResponseDescription.NO_CONTENT.value
    },
    response_model=dict,
    status_code=status.HTTP_200_OK
)

recovery_password = AuthenticationUrlConfig(
    tags=['user'],
    name='Восстановление пароля',
    description='Восстановление пароля',
    responses={
        status.HTTP_403_FORBIDDEN: ResponseDescription.NO_CONTENT.value,
        status.HTTP_204_NO_CONTENT: ResponseDescription.NO_CONTENT.value
    },
    response_model=dict,
    status_code=status.HTTP_200_OK
)
