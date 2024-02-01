"""CDEK Routers"""
from fastapi import APIRouter


common_router = APIRouter(prefix="/delivery", tags=["General"])

@common_router.get("/")
async def check_delivery():
    """Получение информации обо всех активных доставках"""
    return {"message": "It works!"}
