"""Модуль взаимодействия с API CDEK для получения наклеек
"""
import asyncio
import json
import os
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

async def get_barcode_url(barcode_id):
    result = await make_request(api, "get", f"{CDEK_URL}/print/barcodes/{barcode_id}")
    url = result.json()["entity"]["url"]
    log.info(url)
    return url

async def get_file(url, uuid):
    base_dir = os.path.abspath(os.getcwd())
    r = await make_request(api, "get", url, timeout=20)
    with open(f'{base_dir}/temp/{uuid}.pdf', 'wb') as f:
        f.write(r.content)

if __name__ == "__main__":
    asyncio.run(get_barcode_url("72753031-00ae-4c7a-86fe-0209a5c060a0"))
