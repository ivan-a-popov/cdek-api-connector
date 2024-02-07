"""Database Module"""
from typing import Generator
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import app.settings as settings


Base = declarative_base()
metadata = MetaData()
engine = create_async_engine(
        settings.DATABASE_URL,
        future=True,
       # echo=True,
    )

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
