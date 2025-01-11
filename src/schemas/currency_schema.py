from pydantic import BaseModel, PositiveInt, ConfigDict


class CurrencySchema(BaseModel):
    id: PositiveInt | None = None
    full_name: str
    code: str
    sign: str

    model_config = ConfigDict(from_attributes=True)  # Позволяет преобразовывать SQLAlchemy объекты в Pydantic