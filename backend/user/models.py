from typing import List

from pydantic import EmailStr
from sqlalchemy.orm import relationship
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
    refresh_tokens: List['BaseRefreshToken'] = Relationship(back_populates='user')
    open_node_links: List['UserNodeMapper'] = Relationship(back_populates='user')
    nodes: 'NodeDataBase' = Relationship(sa_relationship=relationship('NodeDataBase', remote_side='author_id'))
    node: 'NodeDataBase' = Relationship(sa_relationship=relationship('NodeDataBase', remote_side='user_id'))


class UpdateUserSchema(SQLModel):
    username: str | None
    email: EmailStr | None
    password: str | None
