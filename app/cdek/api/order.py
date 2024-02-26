"""API CDEK module, working with 'order' entity"""
import json
from datetime import datetime
from sqlalchemy import text, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Delivery
from app.cdek.schemas.delivery import DeliveryOrder
from app.cdek.api.auth import ApiService, make_request
from app.core.logger import log
from app.core.settings import CDEK_URL
from app.database.reflection import Order

api = ApiService()

async def create_order(q: DeliveryOrder, session: AsyncSession):
    """Create delivery order"""
    data = q.model_dump(exclude={'crm_id', 'wms_id'})
    payload = json.dumps(data, default=str, ensure_ascii=False)
    log.info(payload)
    responce = await make_request(api, "post", f"{CDEK_URL}/orders", content=payload)
    r = responce.json()
    log.info(r)
    order = Delivery(
        id = int(q.wms_id),
        crm_id = q.crm_id,
        number = (q.number),
        tk_name = "CDEK",
        tk_id = r['entity']['uuid'],
        tk_status = r['requests'][0]['state'],
        updated = datetime.now() # r['requests'][0]['date_time']),
    )
    session.add(order)
    await session.commit()
    return order

async def check_order(order_id, session: AsyncSession):
    """Check delivery order status"""
    result = await session.execute(text(f'select * from "delivery_api" where "id" = {order_id}'))
    row = result.first()
    if row:
        response = await make_request(api, "get", f"{CDEK_URL}/orders/?im_number={row.number}")
        r = response.json()
        data = {"id": int(order_id)}
        data["tk_status"] = r['entity']['statuses'][0]['code']
        data["updated"] = datetime.now() # response.json()['entity']['statuses'][0]['date_time']
        if data["tk_status"] == "INVALID":
            data["errors"] = ",".join(str(element) for element in r['requests'][0]['errors'])
        await session.execute(update(Delivery), [data])
        await session.execute(update(Order),[{"id": int(order_id), "IsUpdated": True}])
        await session.commit()
        return r
    else:
        return None
