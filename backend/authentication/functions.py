import datetime
import hashlib

from datetime import timedelta

from backend.authentication.crud import RefreshTokenCrud
from backend.authentication.schemas import BaseRefreshTokenSchema
from backend.core.additional import create_token
from backend.core.config import project_config


def hash_password(password) -> bytes:
    return hashlib.pbkdf2_hmac(
        'sha256',  # Используемый алгоритм хеширования
        password.encode('utf-8'),  # Конвертирование пароля в байты
        project_config['authentication']['salt'].encode(),  # Предоставление соли
        100000,  # Рекомендуется использоваться по крайней мере 100000 итераций SHA-256
        dklen=128  # Получает ключ в 128 байтов
    )


def create_registration_token(user_id: str) -> str:
    return create_token({'user_id': user_id}, timedelta(days=15))


def create_password_recovery_token(user_id: str) -> str:
    return create_token({'user_id': user_id, 'recovery': True}, timedelta(minutes=15))


def create_login_token(user_id: str) -> str:
    return create_token({'user_id': user_id}, timedelta(minutes=10))


def create_refresh_token(user_id: str) -> BaseRefreshTokenSchema:
    return BaseRefreshTokenSchema(user_id=user_id, time_out=datetime.datetime.utcnow() + timedelta(days=90))


def get_refresh_cookies_age(days: int) -> int:
    return days * 24 * 60 * 60


async def update_refresh_token(refresh_token: str) -> str | None:
    crud = RefreshTokenCrud()
    database_refresh_token = await crud.get(refresh_token)
    if database_refresh_token and database_refresh_token['time_out'] > datetime.datetime.utcnow():
        if await crud.update(refresh_token, {'time_out': datetime.datetime.utcnow() + timedelta(days=90)}):
            return create_login_token(database_refresh_token['user_id'])
        else:
            return None
    else:
        return None


async def new_refresh_token(user_id: str) -> str:
    crud = RefreshTokenCrud()
    tokens = await crud.get_by_user_id(user_id)
    if len(tokens) > 2:
        await crud.delete(sorted(tokens, key=lambda x: x['time_out'])[0]['id'])
    return await crud.create(create_refresh_token(user_id).dict())
