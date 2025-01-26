from pydantic import BaseModel, PositiveInt, ConfigDict, Field


class CurrencySchema(BaseModel):
    id: PositiveInt | None = None
    full_name: str = Field(..., serialization_alias="name")
    code: str
    sign: str

    model_config = ConfigDict(from_attributes=True)  # Позволяет преобразовывать SQLAlchemy объекты в Pydantic