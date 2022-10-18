from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database.config import database_url


engine = None


def init_db():
    global engine
    engine = create_async_engine(database_url, echo=True, future=True)


def get_engine():
    global engine
    return engine


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        get_engine(), class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        return session


