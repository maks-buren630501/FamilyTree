from pydantic import BaseSettings

from backend.core.config import project_config


class DatabaseAuth(BaseSettings):
    database_user: str = project_config['database']['mongo_user']
    password: str = project_config['database']['mongo_password']

    class Config:
        frozen = True


data_base_auth = DatabaseAuth()

mongo_url = f'mongodb+srv://{data_base_auth.database_user}:{data_base_auth.password}@cluster0.dkda1.mongodb.net/FamilyTree?retryWrites=true&w=majority'
