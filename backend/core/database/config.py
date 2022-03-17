from pydantic import BaseSettings, Field


class DatabaseAuth(BaseSettings):
    user: str = Field(..., env='mongo_user')
    password: str = Field(..., env='mongo_password')

    class Config:
        frozen = True


data_base_auth = DatabaseAuth()

mongo_url = f'mongodb+srv://{data_base_auth.user}:{data_base_auth.password}@cluster0.dkda1.mongodb.net/FamilyTree?retryWrites=true&w=majority'
