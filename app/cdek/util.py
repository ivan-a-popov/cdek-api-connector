"""Helper functions for CDEK"""
import re
# from app.core.logger import log

from app.retailcrm.api import get_crm_info
from app.database.accessor import get_weight
from app.cdek.schemas.delivery import DeliveryOrder


def extract_pvz_id(text):
    """Parce comment trying to find PVZ ID"""
    pattern = r'([A-Z]{3,6}\d{1,4})'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None


async def make_package(data, db):
    """Fill package with items"""
    items = []
    for item in data["order"]["items"]:
        product = {}
        product["ware_key"] = item["offer"]["article"]
        product["name"] = item["offer"]["name"]
        product["payment"] = {"value": item["prices"][0]["price"]}
        product["cost"] = item["prices"][0]["price"]
        product["amount"] = item["quantity"]
        product["weight"] = await get_weight(product["ware_key"], db)
        items.append(product)
    return items


async def make_delivery(order, db):
    """Prepare DeliveryOrder object"""
    crm_info = await get_crm_info(order.CrmId)
    recipient = {
        "name": f'{crm_info["order"]["firstName"]} {crm_info["order"]["lastName"]}',
        "phones": crm_info["order"]["contact"]["phones"],
    }
    delivery = DeliveryOrder(
        wms_id=order.id,
        crm_id=order.CrmId,
        number=crm_info["order"]["number"],
        tariff_code=int(crm_info["order"]["delivery"]["data"]["tariff"]),
        recipient=recipient
    )
    text = crm_info["order"]["customerComment"]
    pvz_id = extract_pvz_id(text)
    if pvz_id:
        delivery.delivery_point = str(pvz_id)
    else:
        delivery.to_location = {"address": order.address}
    delivery.packages = [{
        "number": "1",
        "weight": crm_info["order"]["weight"],
        "height": int(crm_info["order"]["height"]/10),
        "length": int(crm_info["order"]["length"]/10),
        "width": int(crm_info["order"]["width"]/10),
        "items": await make_package(crm_info, db),
    },]
    return delivery
