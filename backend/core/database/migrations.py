import os

from sqlmodel import SQLModel

from core.database.driver import get_engine


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
    os.mkdir('migrations/versions')
    os.system(f'alembic revision --autogenerate -m "init"')


def migrate():
    os.system(f'alembic upgrade head')



