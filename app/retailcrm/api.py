"""
Позвонить за день до доставки(желательно)
Спасибо ???? 
[DB]
Тип доставки: ПВЗ СДЭК
ПВЗ ID MSK202
ПВЗ адрес: Example Region, Example City, Example Street, 1
Срок доставки: 5 дней
Стоимость доставки: 312р.
[/DB]

100001 -- pickup order
100002 -- courier order
"""

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
