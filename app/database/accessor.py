"""DAL module"""
from datetime import datetime
from sqlalchemy import insert, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Delivery
from app.database.reflection import Order, Product
from app.core.logger import log


async def get_order_by_id(order_id, sess: AsyncSession):
    """Fetch order from DB by inner id"""
    async with sess as session:
        stmt = select(Order).where(Order.id == int(order_id))
        result = await session.execute(stmt)
        order = result.scalars().first()
        return order

async def get_order_by_number(number, sess: AsyncSession):
    """Fetch order from DB by RetalCRM number"""
    async with sess as session:
        stmt = select(Order).where(Order.numberOrder == number)
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

async def save_url(url, uuid, session: AsyncSession):
    result = await session.execute(
        text(f'update "delivery_api" set "print_file" = \'{url}\' where "tk_uuid" = \'{uuid}\'')
        )
    await session.commit()
    return result

async def save_delivery(data, session: AsyncSession):
    data["updated"] = datetime.now()
    try:
        await session.execute(insert(Delivery), data)
    except Exception:
        await session.rollback()
        await session.execute(update(Delivery), [data])
    finally:
        await session.commit()
