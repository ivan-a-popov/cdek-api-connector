from pydantic import BaseModel


class Attr(BaseModel):
    type: str
    url: str

class PrintForm(BaseModel):
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
    type: str
    date_time: str
    uuid: str
    attributes: Attr
