from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal

from src.schemas.currency_schema import CurrencySchema


class ExchangeSchema(BaseModel):
    base_currency: CurrencySchema
    target_currency: CurrencySchema
    rate: Decimal = Field(max_digits=9, decimal_places=6)
    amount: Decimal = Field(max_digits=9, decimal_places=6)
    converted_amount: Decimal = Field(max_digits=9, decimal_places=6)

    model_config = ConfigDict(from_attributes=True)  # Позволяет преобразовывать SQLAlchemy объекты в Pydantic
