from pydantic import BaseModel, Field, PositiveInt


class CurrencySchema(BaseModel):
    id: PositiveInt | None = None
    name: str
    code: str
    sign: str
