"""Модуль взаимодействия с API CDEK для получения наклеек
"""
import asyncio
import json
from app.cdek.api.auth import ApiService, make_request
from app.core.settings import CDEK_URL
from app.core.logger import log

api = ApiService()

async def create_barcode(order_id):
    data = {
    "orders": [
        {
            "order_uuid": order_id
		}
	],
    "copy_count": 1,
    "format": "A7"
}
    payload = json.dumps(data, default=str, ensure_ascii=False)
    response = await make_request(api, "post", f"{CDEK_URL}/print/barcodes", content=payload)
    r = response.json()["entity"]["uuid"]
    return r

async def get_barcode(barcode_id):
    result = await make_request(api, "get", f"{CDEK_URL}/print/barcodes/{barcode_id}")
    url = result.json()["entity"]["url"]
    log.info(url)
    return r

if __name__ == "__main__":
    asyncio.run(get_barcode("72753031-08f5-4b7d-863d-9d3ff51dbe25"))
