import datetime
import uuid
from datetime import date
from typing import List

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, RelationshipProperty
from sqlmodel import SQLModel, Field, Relationship
from sqlmodel.sql.sqltypes import GUID

from core.database.models import BaseModel
from user.models import UserDataBase


class PartnersMapper(BaseModel, SQLModel, table=True):
    husband_id: uuid.UUID = Field(sa_column=Column(GUID, ForeignKey('nodedatabase.id', ondelete="CASCADE")))
    husband: 'NodeDataBase' = Relationship(sa_relationship=RelationshipProperty("NodeDataBase", foreign_keys=[husband_id]))
    wife_id: uuid.UUID = Field(sa_column=Column(GUID, ForeignKey('nodedatabase.id', ondelete="CASCADE")))
    wife: 'NodeDataBase' = Relationship(sa_relationship=RelationshipProperty("NodeDataBase", foreign_keys=[wife_id]))

    wedding_date: datetime.date | None
    divorce_date: datetime.date | None


class UserNodeMapper(BaseModel, SQLModel, table=True):
    user_id: uuid.UUID = Field(sa_column=Column(GUID, ForeignKey(UserDataBase.id, ondelete="CASCADE")))
    user: UserDataBase = Relationship(back_populates='open_node_links')
    node_id: uuid.UUID = Field(sa_column=Column(GUID, ForeignKey('nodedatabase.id', ondelete="CASCADE")))
    node: 'NodeDataBase' = Relationship(back_populates='user_links')


class BaseNodeSchema(SQLModel):
    name: str
    family_name: str
    old_family_name: str | None
    father_name: str | None
    birthday: date | None
    death_date: date | None
    photo: str | None
    information: str | None

    user_id: uuid.UUID | None = Field(sa_column=Column(GUID, ForeignKey(UserDataBase.id, ondelete="CASCADE"), unique=True))

    father_id: uuid.UUID | None = Field(sa_column=Column(GUID, ForeignKey('nodedatabase.id'), nullable=True))
    mother_id: uuid.UUID | None = Field(sa_column=Column(GUID, ForeignKey('nodedatabase.id'), nullable=True))

    @property
    def params(self):
        return self.__dict__


class NodeDataBase(BaseModel, BaseNodeSchema, table=True):

    author_id: uuid.UUID = Field(sa_column=Column(GUID, ForeignKey(UserDataBase.id, ondelete="CASCADE"), nullable=False))
    author: UserDataBase = Relationship(sa_relationship=RelationshipProperty("UserDataBase", foreign_keys=[author_id]))

    user: UserDataBase = Relationship(sa_relationship=RelationshipProperty("UserDataBase", foreign_keys=['user_id']))
    user_links: List[UserNodeMapper] = Relationship(back_populates='node')

    father: 'NodeDataBase' = Relationship(sa_relationship=relationship('NodeDataBase', remote_side=id))
    mother: 'NodeDataBase' = Relationship(sa_relationship=relationship('NodeDataBase', remote_side=id))

    # children: List['NodeDataBase'] = Relationship()
    # partners: List['NodeDataBase'] = Relationship(link_model=PartnersMapper)






