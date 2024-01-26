"""Database Module"""
import asyncio
from sqlalchemy.types import UUID
from sqlalchemy import MetaData, select, text
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine
import app.settings as settings


Base = declarative_base()
metadata = MetaData()
engine = create_async_engine(
        settings.DATABASE_URL,
        future=True,
       # echo=True,
    )

# async_session = AsyncSession(engine, expire_on_commit=False)

class Cdek(Base):
    """DB model for delivery object"""
    __tablename__ = "cdek_integration"
    id: Mapped[int] = mapped_column(primary_key=True)
    cdek_id: Mapped[UUID] = mapped_column(UUID)


async def test_core():
    """Test function to check DB connenction"""
    async with engine.connect() as connection:
        print("Connected successfully!")
        # result = await connection.execute(text("select * from customer where firstname = 'Анна'"))
        result = await connection.execute(text('select * from "deliveryType"'))
        for row in result:
            print(row)


async def test_orm():
    """Test function to check DB connenction"""
    async with engine.begin() as conn:
        print("Connected successfully!")

        # Reflect all tables
        await conn.run_sync(metadata.reflect)

        # Get the list of table names
        table_names = metadata.tables.keys()
        # Print the table names
        print("Tables in the database:")
        for table_name in table_names:
            print(table_name)

        # select an order
        order_table = metadata.tables['order']
        result = await conn.execute(select(order_table.c.address).where(order_table.c.id == 781))
        address = result.fetchone()
        print(address)
        await engine.dispose()


if __name__ == '__main__':
    # asyncio.run(test_orm())
    asyncio.run(test_core())
