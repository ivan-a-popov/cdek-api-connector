"""Модуль взаимодействия с API CDEK"""
import json
from sqlalchemy import text, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Delivery
from app.cdek.schemas.delivery import DeliveryOrder
from app.cdek.api.auth import ApiService, make_request
from app.core.logger import log
from app.core.settings import CDEK_URL
from app.database.reflection import Order

api = ApiService()

async def create_order(q: DeliveryOrder, db: AsyncSession):
    """Создать заявку на доставку"""
    data = q.model_dump(exclude={'crm_id'})
    payload = json.dumps(data, default=str, ensure_ascii=False)
    log.info(payload)
    responce = await make_request(api, "post", f"{CDEK_URL}/orders", content=payload)
    r = responce.json()
    log.info(r)
    session = db
    order = Delivery(
        id = int(q.number),
        crm_id = q.crm_id,
        ext_service = "CDEK",
        ext_id = r['entity']['uuid'],
        ext_status = r['requests'][0]['state'],
        ext_uuid = r['requests'][0]['request_uuid'],
        time = r['requests'][0]['date_time'],
    )
    log.info(order)
    session.add(order)
    await session.commit()
    return r

async def check_order(order_id, db: AsyncSession):
    """Проверить статус заявки на доставку"""
    session = db
    result = await session.execute(text(f'select * from "delivery_api" where "id" = {order_id}'))
    row = result.first()
    log.info(row)
    response = await make_request(api, "get", f"{CDEK_URL}/orders/{row.ext_id}")
    log.info(response.json())
    status = response.json()['entity']['statuses'][0]['code']
    time = response.json()['entity']['statuses'][0]['date_time']
    await session.execute(update(Delivery),
                          [{"id": int(order_id), "ext_status": status, "time": time}]
                          )
    await session.execute(update(Order),[{"id": int(order_id), "managerComment": "Yeah, baby!"}])
    await session.commit()
    return response.json()
