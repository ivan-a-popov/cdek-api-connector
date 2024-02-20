from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Delivery
from app.cdek.schemas.delivery import DeliveryOrder
from app.database.reflection import Order, Product
from app.core.logger import log


async def save_order(order, db: AsyncSession):
    """Создать заявку на доставку"""
    session = db
    order = Delivery(
        id = int(order.number),
        crm_id = order.crm_id,
        service = "CDEK",
        service_id = order['entity']['uuid'],
        service_status = order['requests'][0]['state'],
        service_uuid = order['requests'][0]['request_uuid'],
        time = order['requests'][0]['date_time'],
    )
    log.info(order)
    session.add(order)
    await session.commit()
    return order

async def get_order(order_id, sess: AsyncSession):
    async with sess as session:
        stmt = select(Order).where(Order.id == int(order_id))
        result = await session.execute(stmt)
        order = result.scalars().first()
        return order

async def get_weight(article, sess: AsyncSession):
    async with sess as session:
        stmt = select(Product.weight).where(Product.article == article)
        result = await session.execute(stmt)
        weight = result.scalars().first()
        print(weight)
        return weight
