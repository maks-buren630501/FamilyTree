from typing import List

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

from core.database.models import BaseModel


class BaseUserSchema(SQLModel):
    username: str
    email: EmailStr = Field(unique=True)


class UserSchemaGet(BaseModel, BaseUserSchema):
    active: bool = Field(default=False)


class UserSchemaCreate(BaseUserSchema):
    password: str


class UserDataBase(UserSchemaGet, table=True):
    password: bytes
    refresh_tokens: List['BaseRefreshToken'] = Relationship(back_populates="user")


class UpdateUserSchema(BaseModel):
    username: str | None
    email: EmailStr | None
    password: str | None
