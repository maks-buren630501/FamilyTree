from pydantic import BaseModel, EmailStr


class BaseUserSchema(BaseModel):
    name: str
    email: EmailStr


class UserSchemaGet(BaseUserSchema):
    id: str


class UserSchemaCreate(BaseUserSchema):
    password: str


class UpdateUserSchema(BaseModel):
    name: str | None
    email: EmailStr | None
    password: str | None


class LoginUserSchema(BaseModel):
    name: str
    password: str
