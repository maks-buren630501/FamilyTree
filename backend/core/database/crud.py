from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select, SelectOfScalar

from core.database.driver import get_session
from core.database.models import BaseModel


class BaseCrud:

    @staticmethod
    async def get(select: Select | SelectOfScalar):
        session: AsyncSession = await get_session()
        result = await session.exec(select)
        return result.first()

    @staticmethod
    async def get_all(select: Select | SelectOfScalar) -> list:
        session: AsyncSession = await get_session()
        result = await session.exec(select)
        return result.all()

    @staticmethod
    async def save(database_object: BaseModel) -> int:
        session: AsyncSession = await get_session()
        session.add(database_object)
        await session.commit()
        await session.refresh(database_object)
        return database_object.id

    @staticmethod
    async def delete(database_object: BaseModel) -> None:
        session: AsyncSession = await get_session()
        await session.delete(database_object)
        await session.commit()
