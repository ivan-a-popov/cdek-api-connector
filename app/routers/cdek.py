"""CDEK Routers"""
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.cdek.schemas.delivery import DeliveryOrder
from app.cdek.api.order import create_order, check_order
import app.cdek.api.barcode as barcode
from app.database.session import get_db
from app.database.accessor import save_url
from app.cdek.schemas.webhooks import PrintForm
from app.core.filer import save_file

cdek_router = APIRouter(prefix="/cdek", tags=["CDEK"])

@cdek_router.post("/orders")
async def create_delivery(body: DeliveryOrder, db: AsyncSession = Depends(get_db)):
    """Создание заказа на доставку СДЭК"""
    r = await create_order(body, db)
    return r

@cdek_router.get("/orders/{order_id}")
async def check_delivery(order_id, db: AsyncSession = Depends(get_db)):
    """Проверить статус заявки на доставку"""
    return await check_order(order_id, db)

@cdek_router.get("/barcode/{order_id}")
"""Создать печатную форму наклейки"""
async def create_barcode(order_id, db: AsyncSession = Depends(get_db)):
    uuid = await barcode.create(order_id, db)
    return uuid

@cdek_router.post("/barcode")
async def recieve_barcode(body: PrintForm, db: AsyncSession = Depends(get_db)):
    """Служебный хэндлер для получения вебхуков от СДЕК"""
    dump = body.model_dump(include={'attributes', 'uuid'})
    uuid = dump['uuid']
    url = dump['attributes']['url']
    link = await save_file(url, uuid)
    r = await save_url(link, uuid, db)
    return r
