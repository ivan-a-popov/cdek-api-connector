"""API CDEK module to create and download barcodes"""
import asyncio
import json
import os
from sqlalchemy import text
from app.cdek.api.auth import ApiService, make_request
from app.core.settings import CDEK_URL
from app.core.logger import log

api = ApiService()

async def create(order_id, session):
    result = await session.execute(text(f'select * from "delivery_api" where "id" = {order_id}'))
    row = result.first()
    data = {
    "orders": [
        {
            "order_uuid": f"{row.tk_id}"
		}
	],
    "copy_count": 1,
    "format": "A7"
}
    payload = json.dumps(data, default=str, ensure_ascii=False)
    response = await make_request(api, "post", f"{CDEK_URL}/print/barcodes", content=payload)
    log.info(response.text)
    r = response.json()["entity"]["uuid"]
    return r

async def get_url(barcode_id):
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
    asyncio.run(get_url("72753031-b281-4270-99b6-6f0ba3792c66"))
