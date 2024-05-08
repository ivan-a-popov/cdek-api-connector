"""Модели для описания контрагента (отправителя, получателя) и связанные модели"""
from datetime import date
from typing import List
from pydantic import BaseModel, Field, EmailStr


class Phone(BaseModel):
    """Номер телефона (мобильный/городской)"""
    number: str = Field(max_length=255,
                                description='Номер телефона. Необходимо передавать в ' \
                                    'международном формате: код страны (для России +7) ' \
                                    'и сам номер (10 и более цифр)')
    additional: str = Field(default=None, max_length=255,
                                description='Дополнительная информация (добавочный номер)')


class Seller(BaseModel):
    """Данные истинного продавца"""
    name: str = Field(default=None, max_length=255,
                                description='Наименование истинного продавца')
    inn: str = Field(default=None, max_length=255,
                                description='ИНН истинного продавца')
    phone: str = Field(default=None, max_length=255,
                                description='Телефон истинного продавца')
    ownership_form: int = Field(default=None,
                                description='Код формы собственности')
    address: str = Field(default=None, max_length=255,
                                description='Адрес истинного продавца. Используется при печати ' \
                                    'инвойсов для отображения адреса настоящего продавца товара, ' \
                                    'либо торгового названия')



class Recipient(BaseModel):
    """Получатель"""
    company: str = Field(default=None, max_length=255,
                                description='Название компании')
    name: str = Field(max_length=255,
                                description='Ф.И.О контактного лица')
    email: EmailStr = Field(default=None,
                               description='Эл. адрес. Должен соответствовать RFC 2822. ' \
                                'Если email указан некорректно, то он будет удалён, а заказ создан')
    phones: List[Phone]
    passport_series: str = Field(default=None, max_length=4,
                                description='Название компании')
    passport_number: str = Field(default=None, max_length=30,
                                description='Название компании')
    passport_date_of_issue: date = Field(default=None,
                               description='Дата выдачи паспорта (yyyy-MM-dd)')
    passport_organization: str = Field(default=None, max_length=255,
                                description='Орган выдачи паспорта')
    passport_date_of_birth: date = Field(default=None,
                               description='Дата рождения (yyyy-MM-dd)')
    tin: str = Field(default=None, max_length=12,
                                description='ИНН. Может содержать 10, либо 12 символов')
    passport_requirements_satisfied: bool = Field(default=None,
                                description='Требования по паспортным данным удовлетворены ' \
                                    '(актуально для международных заказов): ' \
                                    '\ntrue - паспортные данные собраны или не требуются' \
                                    '\nfalse - паспортные данные требуются и не собраны')
