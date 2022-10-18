import asyncio

from sqlmodel import SQLModel

from core.database.driver import get_engine
from authentication import models
from user import models


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


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coroutine = create_db_and_tables()
    loop.run_until_complete(coroutine)
