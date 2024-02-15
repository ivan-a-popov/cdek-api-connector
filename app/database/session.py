"""Database Module"""
from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import app.core.settings as settings


async_engine = create_async_engine(
        settings.db_async_url,
        future=True,
       # echo=True,
    )

async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
