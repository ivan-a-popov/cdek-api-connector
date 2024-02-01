"""Модуль взаимодействия с API CDEK"""
import asyncio
import json
from time import sleep

from pydantic_core import to_json
from app.logger import log
from app.settings import CDEK_URL
from app.cdek.schemas.delivery import DeliveryOrder
from app.cdek.api.auth import ApiService

api = ApiService()

# async def test_usage(api, i):
#     """Test function for API auth"""
#     try:
#         response = await api.make_request("get", f"{CDEK_URL}/location/regions")
#     except Exception as e:
#         log.error('Error: %s', e)
#         return
#     log.info((response.json()[i]))

async def create_order(q: DeliveryOrder):
    data = q.model_dump(exclude={'crm_id'})
    payload = json.dumps(data, default=str)
    print(type(payload))
    response = await api.make_request("post", f"{CDEK_URL}/orders", content=payload)
    # Now you can use order_without_crm_id directly in your external API query
    print(response.text)


# Run the example usage within an asynchronous context
# if __name__ == "__main__":
#     for i in range(100):
#         asyncio.run(test_usage(api, i))
#         sleep(10)
