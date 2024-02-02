"""Основная модель доставки СДЭК и непосредственно связанные модели"""
from datetime import date
from typing import List
from pydantic import BaseModel, Field
from app.cdek.schemas.location import Location
from app.cdek.schemas.money import Money, Threshold
from app.cdek.schemas.contact import Recipient, Seller
from app.cdek.schemas.package import Package


class Service(BaseModel):
    """Дополнительная услуга"""
    code: str = Field(description='Код дополнительной услуги')
    parameter: str = Field(default=None,
                           description='Параметр дополнительной услуги')

class DeliveryOrder(BaseModel):
    """Модель, описывающая объект доставки"""
    crm_id: int = Field(description='ID заказа в RetaiCRM')
    number: str = Field(max_length=40, description='WMS order ID')
    tariff_code: int = Field(description='Код тарифа. Подробнее см. приложение 1: ' \
                             'https://api-docs.cdek.ru/29923926.html')    
    comment: str = Field(default=None, description='Комментарий к заказу')
    shipment_point: str = Field(default='MSK342', max_length=255,
                                description='Код ПВЗ СДЭК, на который будет производиться ' \
                                    'самостоятельный привоз клиентом. Не может использоваться ' \
                                    'одновременно с from_location')
    delivery_point: str = Field(default=None, max_length=255,
                                description='Код офиса СДЭК (ПВЗ/постамата), на который будет ' \
                                    'доставлена посылка (Не может использоваться ' \
                                    'одновременно с to_location)')
    date_invoice: date = Field(default=None,
                               description='Дата инвойса (yyyy-MM-dd). Только для международных ' \
                                    'заказов  с типом "интернет-магазин". Если поле заполнено, ' \
                                    'то заказ автоматически становится международным.')
    shipper_name: str = Field(default=None, max_length=255,
                              description='ГрузоотправительТолько для международных заказов с ' \
                                    'типом "интернет-магазин". Если поле заполнено, то заказ ' \
                                    'автоматически становится международным. ')
    shipper_address: str = Field(default=None, max_length=255,
                                 description='Адрес грузоотправителя. Только для международных ' \
                                    'заказов с типом "интернет-магазин". Если поле заполнено, ' \
                                    'то заказ автоматически становится международным. ')
    delivery_recipient_cost: Money(default=None,
                                   description='Доп. сбор за доставку, которую ИМ берет с ' \
                                    'получателя. Только для заказов "интернет-магазин".')
    delivery_recipient_cost_adv: List[Threshold] = Field(default=None,
                                           description='Доп. сбор за доставку, который ИМ берет ' \
                                    'с получателя) в зависимости от суммы заказа. Только для ' \
                                    'заказов "интернет-магазин". Возможно указать несколько ' \
                                    'порогов.')
    seller: Seller = Field(default=None, description='Обязательно, если заказ международный')
    recipient: Recipient = Field(description='Получатель')
    # from_location: Location = Field(default=None,
                                # description='Адрес отправления. Не может использоваться ' \
                                    # 'одновременно с shipment_point')
    to_location: Location = Field(default=None,
                                description='Адрес получения. Не может использоваться ' \
                                    'одновременно с delivery_point')
    services: List[Service] = Field(default=None,
                                description='Дополнительные услуги')
    packages: List[Package] = Field(description='Список информации по местам (упаковкам). ' \
                                    'Количество мест в заказе может быть от 1 до 255')
    print: str = Field(default='barcode', description='Необходимость сформировать печатную ' \
                                     'форму по заказу')
