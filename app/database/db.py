"""Database Module"""
from typing import Generator
from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import app.settings as settings


metadata = MetaData()
engine = create_engine(settings.db_url)
"""We're going to use the automap extension to automatically reflect database tables to SQLAlchemy 
models. However automap uses 'inspect' on the engine, and this isn't supported on async engines; 
we can work around this by doing the automapping using a synchronous engine. Once the models have 
been mapped they can be used by the async engine.
"""

metadata.reflect(engine, only=['order'])
Base = automap_base(metadata=metadata)

# reflect the tables
Base.prepare(autoload_with=engine)

# mapped classes are now created with names by default
# matching that of the table name.
Order = Base.classes.order


async_engine = create_async_engine(
        settings.db_async_url,
        future=True,
       # echo=True,
    )

async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
