import asyncio
from sqlalchemy import select, text
from app.database.session import engine, metadata


async def test_core():
    """Test function to check DB connenction"""
    async with engine.connect() as connection:
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
        result = await conn.execute(select(order_table.c.address).where(order_table.c.id == 100001))
        address = result.fetchone()
        print(address)


if __name__ == '__main__':
    asyncio.run(test_orm())
    # asyncio.run(test_core())
