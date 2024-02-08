import asyncio
from sqlalchemy import MetaData
from alembic import autogenerate
from alembic.operations import ops
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
import app.settings as settings

Base = declarative_base()
metadata = MetaData()
engine = create_async_engine(
        settings.db_async_url,
        future=True,
       # echo=True,
    )


async def test_orm():
    """Test function to check DB connenction"""
    async with engine.begin() as conn:
        print("Connected successfully!")

        # Reflect all tables
        await conn.run_sync(metadata.reflect)
            
        print(autogenerate.render_python_code(
        ops.UpgradeOps(
            ops=[
                ops.CreateTableOp.from_table(table) for table in metadata.tables.values()
            ] + [
                ops.CreateIndexOp.from_index(idx) for table in metadata.tables.values()
                for idx in table.indexes
            ]
        ))
    )

if __name__ == '__main__':
    asyncio.run(test_orm())