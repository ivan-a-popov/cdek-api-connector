"""34092 -- заказ с адресом
34078 -- заказ с ПВЗ
"""
import re
from app.retailcrm.api import get_crm_info
from app.database.models import Delivery
from app.cdek.schemas.delivery import DeliveryOrder


def extract_pvz_id(text):
    """Parce comment trying to find PVZ ID"""
    pattern = r'ПВЗ ID ([A-Z]{3,6}\d{1,4})'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None


async def make_delivery(order):
    """Prepare DeliveryOrder object"""
    crm_info = await get_crm_info(order.CrmId)
    recipient = {
        "name": f'{crm_info["order"]["contact"]["firstName"]} {crm_info["order"]["contact"]["lastName"]}',
        "phones": crm_info["order"]["contact"]["phones"],
    }
    print(recipient)
    delivery = DeliveryOrder(
        number=crm_info["order"]["number"],
        tariff_code=int(crm_info["order"]["delivery"]["data"]["tariff"]),
        recipient=recipient
    )
    text = crm_info["order"]["customerComment"]
    pvz_id = extract_pvz_id(text)
    if pvz_id:
        delivery.delivery_point = str(pvz_id)
    else:
        delivery.to_location = order.address
    print(delivery)
    # result = Delivery
    responce = {'status': 'OK',
    'order_id': order.id,
    'crm_id': order.CrmId,
    'deliverytype': order.DeliveryTypeId,
    }
    return responce
