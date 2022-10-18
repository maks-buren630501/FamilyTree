import datetime

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

from core.database.models import BaseModel
from user.models import UserDataBase


class UpdatePasswordSchema(SQLModel):
    password: str


class RecoveryPasswordSchema(SQLModel):
    email: EmailStr


class LoginUserSchema(SQLModel):
    username: str
    password: str


class BaseRefreshToken(BaseModel, table=True):
    user_id: int = Field(foreign_key=UserDataBase.id)
    user: UserDataBase = Relationship(back_populates="refresh_tokens")
    time_out: datetime.datetime
