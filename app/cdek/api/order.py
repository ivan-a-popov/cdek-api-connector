"""API CDEK module, working with 'order' entity"""
import json
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Delivery
from app.cdek.schemas.delivery import DeliveryOrder
from app.cdek.api.auth import ApiService, make_request
from app.core.logger import log
from app.core.settings import CDEK_URL
from app.database.accessor import get_order_by_id, save_delivery

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
    try:
        session.add(order)
        await session.commit()
        return order
    except KeyError as e:
        raise HTTPException(
            status_code=409, detail="Delivery order already exists in database") from e

async def check_order(order_id, session: AsyncSession):
    """Check delivery order status"""
    data = {"id": int(order_id)}
    result = await session.execute(text(f'select * from "delivery_api" where "id" = {order_id}'))
    row = result.first()
    if row:
        response = await make_request(api, "get", f"{CDEK_URL}/orders/?im_number={row.number}")
        r = response.json()
        data["tk_status"] = r['entity']['statuses'][0]['code']
        if data["tk_status"] == "INVALID":
            data["errors"] = ",".join(str(element) for element in r['requests'][0]['errors'])
        await save_delivery(data, session)
        return row.tk_id
    else:
        order = await get_order_by_id(order_id, session)
        if order.DeliveryTypeId != 21:
            raise HTTPException(status_code=422, detail="Delivery type is not supported")
        else:
            response = await make_request(
                api, "get", f"{CDEK_URL}/orders/?im_number={order.numberOrder}"
                )
            r = response.json()
            try:
                data["tk_status"] = r['entity']['statuses'][0]['code']
                data["tk_id"] = r['entity']['uuid']
                data["number"] = order.numberOrder
                data["crm_id"] = order.CrmId
                data["tk_name"] = "CDEK"
                await save_delivery(data, session)
                return data["tk_id"]
            except KeyError as e:
                raise HTTPException(status_code=404, detail="Delivery order not found") from e
            