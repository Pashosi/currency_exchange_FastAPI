from pydantic import BaseModel, PositiveInt, ConfigDict, Field
from decimal import Decimal

from src.schemas.currency_schema import CurrencySchema


class ExchangeRateSchema(BaseModel):
    id: PositiveInt | None = None
    base_currency: CurrencySchema
    target_currency: CurrencySchema
    rate: Decimal = Field(max_digits=6, decimal_places=2)

    model_config = ConfigDict(from_attributes=True)  # Позволяет преобразовывать SQLAlchemy объекты в Pydantic


class ExchangeRateCreateSchema(BaseModel):
    id: PositiveInt | None = None
    base_currency: int
    target_currency: int
    rate: Decimal = Field(max_digits=6, decimal_places=2)

    model_config = ConfigDict(from_attributes=True)  # Позволяет преобразовывать SQLAlchemy объекты в Pydantic