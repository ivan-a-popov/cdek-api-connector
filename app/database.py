"""Database Module"""
import asyncio
from typing import Optional
from sqlalchemy.types import UUID
from sqlalchemy import BigInteger, ForeignKey, MetaData, select, text
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
    """DB model for CDEK"""
    __tablename__ = "cdek_integration"
    id: Mapped[BigInteger] = mapped_column(ForeignKey("order.id"), primary_key=True)
    crm_id: Mapped[int] = mapped_column()
    cdek_id: Mapped[Optional[UUID]] = mapped_column(UUID)
    # cdek_status: Mapped[Optional[str]] =

async def test_core():
    """Test function to check DB connenction"""
    async with engine.connect() as connection:
        print("Connected successfully!")
        result = await connection.execute(text('select * from "order" where "DeliveryTypeId" = 21'))
        # result = await connection.execute(text('select * from "deliveryType"'))
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
