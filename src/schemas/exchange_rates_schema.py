from pydantic import BaseModel, PositiveInt, ConfigDict, Field, field_serializer
from decimal import Decimal

from src.schemas.currency_schema import CurrencySchema


class ExchangeRateSchema(BaseModel):
    id: PositiveInt | None = None
    base_currency: CurrencySchema = Field(..., serialization_alias='baseCurrency')
    target_currency: CurrencySchema = Field(..., serialization_alias='targetCurrency')
    rate: Decimal = Field(max_digits=9, decimal_places=6, gt=0)

    model_config = ConfigDict(from_attributes=True)  # Позволяет преобразовывать SQLAlchemy объекты в Pydantic

    # Кастомный сериализатор для вывода rate с двумя знаками после запятой
    @field_serializer("rate")
    def format_rate(self, value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"))
