"""CDEK Routers"""
from fastapi import APIRouter
from app.cdek.schemas.delivery import DeliveryOrder
from app.cdek.api.order import create_order

cdek_router = APIRouter(prefix="/cdek", tags=["CDEK"])

@cdek_router.post("/orders")
async def create_delivery(body: DeliveryOrder):
    """Создание заказа на доставку СДЭК"""
    await create_order(body)
    return {"message": "The query is OK."}
