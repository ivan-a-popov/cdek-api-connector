"""Common Routers"""
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.database.accessor import get_order_by_id
from app.cdek.util import make_delivery
from app.cdek.api.order import create_order


common_router = APIRouter(prefix="/delivery", tags=["General"])

@common_router.get("/{order_id}")
async def create_delivery(order_id, db: AsyncSession = Depends(get_db)):
    """Простое создание доставки"""
    order = await get_order_by_id(order_id, db)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found in database")
    elif order.DeliveryTypeId != 21:
        raise HTTPException(status_code=422, detail="Delivery type is not supported")
    else:
        delivery = await make_delivery(order, db)
        responce = await create_order(delivery, db)
    return responce
