"""RetailCRM client."""
import httpx
from app.core.settings import CRM_API, CRM_URL


async def get_crm_info(order_id):
    params = {'apiKey': CRM_API, 'by': 'id'}
    r = httpx.get(f'{CRM_URL}/orders/{order_id}', params=params)
    return r.json()


if __name__ == "__main__":
    r = get_crm_info(100001)
    for item in r["order"]["items"]:
        print(item)
