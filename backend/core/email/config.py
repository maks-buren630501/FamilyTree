from pydantic import BaseSettings, Field


class MailAuth(BaseSettings):
    user: str = Field(..., env='mail_user')
    password: str = Field(..., env='mail_password')

    class Config:
        frozen = True


mail_auth = MailAuth()
