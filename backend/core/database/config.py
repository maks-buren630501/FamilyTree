from pydantic import BaseSettings

from core.config import project_config


class DatabaseAuth(BaseSettings):
    database_type: str = project_config['database']['type']
    database_user: str = project_config['database']['user']
    password: str = project_config['database']['password']
    host: str = project_config['database']['host']
    port: int = project_config['database']['port']
    database_name: str = project_config['database']['database_name']

    class Config:
        frozen = True


data_base_auth = DatabaseAuth()

database_url = f"{data_base_auth.database_type}://{data_base_auth.database_user}:" \
               f"{data_base_auth.password}@{data_base_auth.host}:{data_base_auth.port}/{data_base_auth.database_name}"
