"""DAL module"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Delivery
from app.database.reflection import Order, Product
from app.core.logger import log


async def get_order(order_id, sess: AsyncSession):
    """Fetch order from DB"""
    async with sess as session:
        stmt = select(Order).where(Order.id == int(order_id))
        result = await session.execute(stmt)
        order = result.scalars().first()
        return order

async def get_weight(article, sess: AsyncSession):
    """Get the item's weight """
    async with sess as session:
        stmt = select(Product.weight).where(Product.article == article)
        result = await session.execute(stmt)
        weight = result.scalars().first()
        print(weight)
        return weight
