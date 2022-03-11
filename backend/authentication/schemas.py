from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class BaseUserSchema(BaseModel):
    name: str
    email: EmailStr


class UserSchemaGet(BaseUserSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}


class UserSchemaCreate(BaseUserSchema):
    password: str


class UpdateUserSchema(BaseModel):
    name: str | None
    email: EmailStr | None
    password: str | None
