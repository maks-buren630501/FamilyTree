import hashlib
import os

from datetime import timedelta

from backend.core.additional import create_token


def hash_password(password):
    return hashlib.pbkdf2_hmac(
        'sha256',  # Используемый алгоритм хеширования
        password.encode('utf-8'),  # Конвертирование пароля в байты
        os.environ['salt'].encode(),  # Предоставление соли
        100000,  # Рекомендуется использоваться по крайней мере 100000 итераций SHA-256
        dklen=128  # Получает ключ в 128 байтов
    )


def create_registration_token(user_id: str):
    return create_token({'user_id': user_id}, timedelta(days=15))





