import asyncio

from sqlmodel import SQLModel

from core.database.driver import engine
from authentication import models
from user import models


async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coroutine = create_db_and_tables()
    loop.run_until_complete(coroutine)
