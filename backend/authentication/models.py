import datetime

from pydantic import EmailStr
from sqlmodel import SQLModel

from core.database.models import BaseModel


class UpdatePasswordSchema(SQLModel):
    password: str


class RecoveryPasswordSchema(SQLModel):
    email: EmailStr


class LoginUserSchema(SQLModel):
    username: str
    password: str


class BaseRefreshTokenSchema(BaseModel, table=True):
    user_id: int
    time_out: datetime.datetime
