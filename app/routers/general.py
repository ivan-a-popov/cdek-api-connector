"""CDEK Routers"""
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.database.accessor import get_order
from app.cdek.util import make_delivery
from app.cdek.api.order import create_order


common_router = APIRouter(prefix="/delivery", tags=["General"])

@common_router.get("/")
async def check_delivery():
    """Получение информации обо всех активных доставках"""
    return {"message": "Not implemented"}

@common_router.post("/{order_id}")
async def create_delivery(order_id, db: AsyncSession = Depends(get_db)):
    """Простое создание доставки"""
    order = await get_order(order_id, db)
    if order.DeliveryTypeId != 21:
        responce = {'status': 'Error',
                    'message': 'Delivery type is not supported',
                    }
    else:
        delivery = await make_delivery(order, db)
        responce = await create_order(delivery, db)
    return responce
