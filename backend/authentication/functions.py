import datetime
import hashlib
import uuid

from datetime import timedelta

from sqlmodel import select

from authentication.models import BaseRefreshToken
from core.additional import create_token
from core.config import project_config
from core.database.crud import Crud


def hash_password(password) -> bytes:
    return hashlib.pbkdf2_hmac(
        'sha256',  # Используемый алгоритм хеширования
        password.encode('utf-8'),  # Конвертирование пароля в байты
        project_config['authentication']['salt'].encode(),  # Предоставление соли
        100000,  # Рекомендуется использоваться по крайней мере 100000 итераций SHA-256
        dklen=128  # Получает ключ в 128 байтов
    )


def create_registration_token(user_id: uuid.UUID) -> str:
    return create_token({'user_id': str(user_id)}, timedelta(days=15))


def create_password_recovery_token(user_id: uuid.UUID) -> str:
    return create_token({'user_id': str(user_id), 'recovery': True}, timedelta(minutes=15))


def create_login_token(user_id: uuid.UUID) -> str:
    return create_token({'user_id': str(user_id)}, timedelta(minutes=10))


def create_refresh_token(user_id: uuid.UUID) -> BaseRefreshToken:
    return BaseRefreshToken(user_id=user_id, time_out=datetime.datetime.utcnow() + timedelta(days=90))


def get_refresh_cookies_age(days: int) -> int:
    return days * 24 * 60 * 60


async def update_refresh_token(refresh_token: str) -> str | None:
    database_refresh_token: BaseRefreshToken = \
        await Crud.get(select(BaseRefreshToken).where(BaseRefreshToken.id == refresh_token))
    if database_refresh_token and database_refresh_token.time_out > datetime.datetime.utcnow():
        database_refresh_token.time_out = datetime.datetime.utcnow() + timedelta(days=90)
        await Crud.save(database_refresh_token)
        return create_login_token(database_refresh_token.user_id)
    else:
        return None


async def new_refresh_token(user_id: uuid.UUID) -> uuid.UUID:
    tokens = await Crud.get_all(select(BaseRefreshToken).where(BaseRefreshToken.user_id == user_id))
    if len(tokens) > 2:
        await Crud.delete(sorted(tokens, key=lambda x: x.time_out)[0])
    return await Crud.save(create_refresh_token(user_id))
