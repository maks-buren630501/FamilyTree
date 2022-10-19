import importlib
import os

from sqlmodel import SQLModel

from core.additional import get_models
from core.database.driver import get_engine


models_list = get_models()
for model in models_list:
    importlib.import_module(model)


async def create_db_and_tables() -> None:
    async with get_engine().begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_tables() -> None:
    async with get_engine().begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


async def clear_tables() -> None:
    async with get_engine().begin() as conn:
        for table in SQLModel.metadata.sorted_tables:
            await conn.execute(table.delete())


def make_migrations():
    os.makedirs(os.environ.get('version_location', 'migrations/versions'), exist_ok=True)
    os.system(f'alembic revision --autogenerate -m "init"')


def migrate():
    os.system(f'alembic upgrade head')


def downgrade(revision='-1'):
    os.system(f'alembic downgrade {revision}')




