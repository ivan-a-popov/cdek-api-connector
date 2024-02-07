"""CDEK Routers"""
from fastapi import APIRouter
from app.cdek.schemas.delivery import DeliveryOrder
from app.cdek.api.order import create_order, check_order
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_db
from fastapi import Depends

cdek_router = APIRouter(prefix="/cdek", tags=["CDEK"])

@cdek_router.post("/orders")
async def create_delivery(body: DeliveryOrder, db: AsyncSession = Depends(get_db)):
    """Создание заказа на доставку СДЭК"""
    r = await create_order(body, db)
    return r

@cdek_router.get("/orders/{order_id}")
async def check_delivery(order_id, db: AsyncSession = Depends(get_db)):
    return await check_order(order_id, db)