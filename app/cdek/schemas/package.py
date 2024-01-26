"""Информация о местах заказа"""
from typing import List
from pydantic import BaseModel, Field
from app.cdek.schemas.money import Money


class Item(BaseModel):
    """информация о товарах места заказа (только для заказа типа "интернет-магазин")"""
    name: str = Field(max_length=255,
                      description='Наименование товара (может также содержать описание ' \
                        'товара: размер, цвет)')
    ware_key: str = Field(max_length=20,
                      description='Идентификатор/артикул товара')
    payment: Money = Field(description='Оплата за товар при получении (за единицу товара ' \
                            'в указанной валюте, значение >=0) — наложенный платеж, в случае ' \
                            'предоплаты значение = 0')
    cost: float = Field(description='Объявленная стоимость товара (за единицу товара в ' \
                            'указанной валюте, значение >=0). С данного значения рассчитывается ' \
                            'страховка')
    weight: int = Field(description='Вес (за единицу товара, в граммах)')
    marking: str = Field(default=None, description='Маркировка товара. Если для товара/вложения ' \
                         'указана маркировка, amount не может быть больше 1.')
    weight_gross: int = Field(default=None, description='Вес брутто')
    amount: int = Field(description='Количество единиц товара (в штуках)')
    name_i18n: str = Field(default=None, max_length=255,
                      description='Наименование на иностранном языке')
    brand: str = Field(default=None, max_length=255,
                      description='Бренд на иностранном языке')
    country_code: str = Field(default=None, max_length=2,
                      description='Код страны в формате  ISO_3166-1_alpha-2')
    material: str = Field(default=None, max_length=255,
                      description='Код материала')
    url: str = Field(default=None, max_length=255,
                      description='	Ссылка на сайт интернет-магазина с описанием товара')

class Package(BaseModel):
    """информация о местах заказа""" 
    number: str = Field(max_length=255,
                      description='Номер упаковки (можно использовать порядковый номер ' \
                        'упаковки заказа или номер заказа), уникален в пределах заказа. ' \
                        'Идентификатор заказа в ИС Клиента')
    weight: int = Field(description='Общий вес (в граммах)')
    length: int = Field(default=None,
                        description='Габариты упаковки. Длина (в сантиметрах)')
    width: int = Field(default=None,
                        description='Габариты упаковки. Ширина (в сантиметрах)')
    height: int = Field(default=None,
                        description='Габариты упаковки. Высота (в сантиметрах)')
    comment: str = Field(default=None, max_length=255,
                      description='Комментарий к упаковке')
    items: List[Item] = Field(description='Позиции товаров в упаковке')
