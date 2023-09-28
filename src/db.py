from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.settings import settings

engine = create_async_engine(settings.db_url)
async_session = async_sessionmaker(engine, autocommit=False, expire_on_commit=False)


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session
