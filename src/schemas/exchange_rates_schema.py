from pydantic import BaseModel, PositiveInt, ConfigDict, Field, field_serializer
from decimal import Decimal

from src.schemas.currency_schema import CurrencySchema


class ExchangeRateSchema(BaseModel):
    id: PositiveInt | None = None
    base_currency: CurrencySchema
    target_currency: CurrencySchema
    rate: Decimal = Field(max_digits=6, decimal_places=2)

    model_config = ConfigDict(from_attributes=True)  # Позволяет преобразовывать SQLAlchemy объекты в Pydantic

    # Кастомный сериализатор для вывода rate с двумя знаками после запятой
    @field_serializer("rate")
    def format_rate(self, value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"))
