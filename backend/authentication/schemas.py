import datetime

from pydantic import BaseModel, EmailStr


class UpdatePasswordSchema(BaseModel):
    password: str


class RecoveryPasswordSchema(BaseModel):
    email: EmailStr


class LoginUserSchema(BaseModel):
    username: str
    password: str


class BaseRefreshTokenSchema(BaseModel):
    user_id: str
    time_out: datetime.datetime
