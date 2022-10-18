import uuid

from sqlalchemy.exc import ProgrammingError, StatementError
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select, SelectOfScalar

from core.database.driver import get_session
from core.database.models import BaseModel


class Crud:

    @staticmethod
    async def base_get(select: Select | SelectOfScalar):
        session: AsyncSession = await get_session()
        try:
            result = await session.exec(select)
        except (ProgrammingError, StatementError):
            return None
        else:
            return result
        finally:
            await session.close()

    @staticmethod
    async def get(select: Select | SelectOfScalar):
        result = await Crud.base_get(select)
        return result.first() if result is not None else None

    @staticmethod
    async def get_all(select: Select | SelectOfScalar) -> list:
        result = await Crud.base_get(select)
        return result.all() if result is not None else []

    @staticmethod
    async def save(database_object: BaseModel) -> uuid.UUID:
        session: AsyncSession = await get_session()
        session.add(database_object)
        await session.commit()
        await session.refresh(database_object)
        await session.close()
        return database_object.id

    @staticmethod
    async def delete(database_object: BaseModel) -> None:
        session: AsyncSession = await get_session()
        await session.delete(database_object)
        await session.commit()
        await session.close()
