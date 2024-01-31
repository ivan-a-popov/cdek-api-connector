"""CDEK Routers"""
from fastapi import APIRouter
from app.cdek.schemas.delivery import DeliveryOrder

cdek_router = APIRouter(prefix="/cdek", tags=["CDEK"])

@cdek_router.post("/orders")
async def create_delivery(body: DeliveryOrder):
    """Создание заказа на доставку СДЭК"""
    # print(body.from_location.fias_guid)
    return {"message": "The query is OK."}
