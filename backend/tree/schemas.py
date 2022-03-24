from datetime import date
from typing import List

from pydantic import BaseModel


class BaseNodeSchema(BaseModel):
    name: str
    family_name: str
    old_family_name: str | None
    father_name: str | None
    birthday: date | None
    death_date: date | None
    photo: str | None
    other_information: dict | None

    author_id: str | None

    father_id: str | None
    mother_id: str | None
    partners: List[str] | None
    children: List[str] | None


class NodeSchemaGet(BaseNodeSchema):
    id: str


class UpdateNodeSchema(BaseModel):
    name: str | None
    family_name: str | None
    old_family_name: str | None
    father_name: str | None
    birthday: date | None
    death_date: date | None
    photo: str | None
    other_information: dict | None

    author_id: str | None

    father_id: str | None
    mother_id: str | None
    partners: List[str] | None
    children: List[str] | None






