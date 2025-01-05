from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import CurrenciesModel
from src.schemas.currency_schema import CurrencySchema


class CurrencyDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_currency(self, code: str):
        try:
            result = await self.session.execute(select(CurrenciesModel).where(CurrenciesModel.code == code))
            result = result.scalars().first()
        # TODO обработка не правильного кода, когда выводится null
        except Exception:
            return {"message": "Ошибка получения валюты"}

        return result

    async def create_currency(self, currency: CurrencySchema):
        new_model = CurrenciesModel(
            code=currency.code,
            full_name=currency.name,
            sign=currency.sign
        )
        self.session.add(new_model)
        try:
            await self.session.commit()
            await self.session.refresh(new_model)
            return new_model
        except Exception:
            return {"message": "Что-то не так"}

    async def get_currencies(self):
        result = await self.session.execute(select(CurrenciesModel))
        return list(result.scalars().all())