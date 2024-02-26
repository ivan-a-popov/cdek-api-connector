from pydantic import BaseModel


class BarcodeAttr(BaseModel):
    type: str
    url: str

class OrderAttr(BaseModel):
    is_return: bool
    cdek_number: str
    number: str = ""
    code: str
    status_code: str
    status_reason_code: str = ""
    status_date_time: str
    city_name: str = ""
    city_code: str = ""

class Webhook(BaseModel):
    type: str
    date_time: str
    uuid: str
    attributes: BarcodeAttr | OrderAttr

class PrintForm(Webhook):
    """
    {
    "type": "PRINT_FORM",
    "date_time": "2019-07-11T13:07:34+0700",
    "uuid": "72753031-8347-40c0-ab0f-1a49c7a262c1",
    "attributes": {
        "type": "barcode",
        "url": "https://api.cdek.ru/v2/print/barcodes/{uuid}.pdf"
    }
    }
    """
    attributes: BarcodeAttr

class OrderUpdate(Webhook):
    """{
  "type": "ORDER_STATUS",
  "date_time": "2020-08-10T21:32:14+0700",
  "uuid": "72753031-2801-4186-a091-0be58cedfee7",
  "attributes": {
    "is_return": false,
    "cdek_number": "1106321645",
	"code": "RECEIVED_AT_SHIPMENT_WAREHOUSE ",
    "status_code": "3",
    "status_date_time": "2020-08-10T21:32:12+0700",
    "city_name": "Новосибирск",
    "city_code": "270"
  }
}
"""
    attributes: OrderAttr
