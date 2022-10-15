from pydantic import BaseSettings

from core.config import project_config


class MailAuth(BaseSettings):
    mail_user: str = project_config['email']['mail_user']
    password: str = project_config['email']['mail_password']

    class Config:
        frozen = True


mail_auth = MailAuth()
