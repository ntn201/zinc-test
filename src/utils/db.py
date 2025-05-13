from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def close_db():
    await engine.dispose()
