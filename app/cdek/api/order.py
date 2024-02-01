"""Модуль взаимодействия с API CDEK"""
import json

from app.logger import log
from app.settings import CDEK_URL
from app.cdek.schemas.delivery import DeliveryOrder
from app.cdek.api.auth import ApiService, make_request

api = ApiService()


async def create_order(q: DeliveryOrder):
    """Создать заявку на доставку"""
    data = q.model_dump(exclude={'crm_id'})
    payload = json.dumps(data, default=str)
    print(type(payload))
    response = await make_request(api, "post", f"{CDEK_URL}/orders", content=payload)
    # Now you can use order_without_crm_id directly in your external API query
    log.info(response.text)
