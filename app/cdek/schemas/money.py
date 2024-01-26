"""Модели для денежных полей"""
from pydantic import BaseModel, Field


class Money(BaseModel):
    """Cтоимость услуги/товара с учетом налогообложения"""
    value: float = Field(default=None,
                         description='Сумма дополнительного сбора (в том числе и НДС)')
    vat_sum: float = Field(default=None,
                           description='Сумма НДС')
    vat_rate: int = Field(default=None,
                           description='Ставка НДС (значение - 0, 10, 12, 20, null - нет НДС)')


class Threshold(BaseModel):
    """Дополнительный сбор за доставку в зависимости от стоимости товара"""
    threshold: int = Field(default=None,
                           description='Порог стоимости товара (действует по условию меньше или ' \
                                    'равно) в целых единицах валюты')
    sum: float = Field(default=None,
                       description='Доп. сбор за доставку товаров, общая стоимость которых ' \
                                    'попадает в интервал (в том числе и НДС)')
    vat_sum: float = Field(default=None,
                           description='Сумма НДС, включённая в доп. сбор за доставку')
    vat_rate: int = Field(default=None,
                           description='Ставка НДС (значение - 0, 10, 12, 20, null - нет НДС)')
