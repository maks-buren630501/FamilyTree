import uuid

from sqlalchemy import Column
from sqlmodel import SQLModel, Field
from sqlmodel.sql.sqltypes import GUID


class BaseModel(SQLModel):
    id: uuid.UUID = Field(sa_column=Column(GUID, primary_key=True, default=uuid.uuid4))

