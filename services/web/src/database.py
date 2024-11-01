from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import Settings


engine = create_async_engine(Settings.DB_URL, future=True, echo=True)

session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator:
    with session_maker() as session:
        yield session

