from pydantic import BaseModel, EmailStr


class BaseUserSchema(BaseModel):
    username: str
    email: EmailStr


class UserSchemaGet(BaseUserSchema):
    id: str


class UserSchemaCreate(BaseUserSchema):
    password: str


class UpdateUserSchema(BaseModel):
    username: str | None
    email: EmailStr | None
    password: str | None
