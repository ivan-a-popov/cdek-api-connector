"""Модель местоположения"""
from uuid import UUID
from pydantic import BaseModel, Field


class Location(BaseModel):
    """Модель местоположения"""
    address: str = Field(max_length=255,
                         description='Строка адреса')
    code: int = Field(default=None,
                      description='Код населенного пункта СДЭК (метод "Список населенных пунктов")')
    fias_guid: UUID = Field(default=None,
                            description='Уникальный идентификатор ФИАС')
    postal_code: str = Field(default=None,
                             description='Почтовый индекс')
    longitude: float = Field(default=None,
                             description='Долгота')
    latitude: float = Field(default=None,
                             description='Широта')
    country_code: str = Field(default=None, max_length=2,
                              description='Код страны в формате  ISO_3166-1_alpha-2')
    region: str = Field(default=None, max_length=255,
                                description='Название региона')
    sub_region: str = Field(default=None, max_length=255,
                                description='Название района региона')
    city: str = Field(default=None, max_length=255,
                                description='Название города')
