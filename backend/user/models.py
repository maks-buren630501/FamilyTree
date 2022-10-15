from pydantic import EmailStr
from sqlmodel import SQLModel, Field

from core.database.models import BaseModel


class BaseUserSchema(SQLModel):
    username: str
    email: EmailStr


class UserSchemaGet(BaseUserSchema):
    id: str


class UserSchemaCreate(BaseUserSchema):
    password: str


class UserDataBase(BaseModel, BaseUserSchema, table=True):
    password: bytes
    active: bool = Field(default=False)


class UpdateUserSchema(BaseModel):
    username: str | None
    email: EmailStr | None
    password: str | None
