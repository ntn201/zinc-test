from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import DATABASE_URL

class Database:
    engine = None
    async_session = None

    @classmethod
    def init_engine(cls):
        cls.engine = create_async_engine(DATABASE_URL)
        cls.async_session = async_sessionmaker(
            cls.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @classmethod
    async def get_session(cls) -> AsyncSession:
        async with cls.async_session() as session:
            yield session

    @classmethod
    async def close_db(cls):
        await cls.engine.dispose()
