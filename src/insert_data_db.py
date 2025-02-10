import asyncio
import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.DAO_currency import CurrencyDAO
from src.dao.DAO_exchange_rates import ExchangeDAO
from src.database import engine, get_db
from src.logging_config import setup_logging

setup_logging()

logger = logging.getLogger('logger')

list_currencies = [
    {"full_name": "UnitedStatesDollar", "code": "USD", "sign": "$"},  # Доллар США
    {"full_name": "Euro", "code": "EUR", "sign": "€"},  # Евро
    {"full_name": "JapaneseYen", "code": "JPY", "sign": "¥"},  # Японская иена
    {"full_name": "BritishPound", "code": "GBP", "sign": "£"},  # Британский фунт стерлингов
    {"full_name": "SwissFranc", "code": "CHF", "sign": "Fr"},  # Швейцарский франк
]

exchange_rates = [
    {"base_currency": "USD", "target_currency": "EUR", "rate": 0.92},
    {"base_currency": "EUR", "target_currency": "USD", "rate": 1.09},
    {"base_currency": "USD", "target_currency": "JPY", "rate": 150.0},
    {"base_currency": "JPY", "target_currency": "USD", "rate": 0.0067},
    {"base_currency": "USD", "target_currency": "GBP", "rate": 0.79},
    {"base_currency": "GBP", "target_currency": "USD", "rate": 1.27},
    {"base_currency": "USD", "target_currency": "CHF", "rate": 0.88},
    {"base_currency": "CHF", "target_currency": "USD", "rate": 1.14},
]


class CreateDataDatabase:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_currencies(self):
        dao = CurrencyDAO(self.session)
        try:
            for currency in list_currencies:
                await dao.create_currency(full_name=currency["full_name"], code=currency["code"], sign=currency["sign"])
        except Exception as e:
            logger.info(f"Базовые валюты уже добавлены, текст:{e}")

    async def add_exchange_rates(self):
        dao = ExchangeDAO(self.session)
        try:
            for exchange_rate in exchange_rates:
                await dao.create_exchange_rate(
                    base_currency_code=exchange_rate["base_currency"],
                    target_currency_code=exchange_rate["target_currency"],
                    rate=exchange_rate["rate"]
                )
        except Exception as e:
            logger.info(f"Базовые обменные курсы уже добавлены, текст:{e}")


async def main():
    async for session in get_db():  # Получаем сессию корректно
        db_obj = CreateDataDatabase(session)
        await db_obj.add_currencies()
        await db_obj.add_exchange_rates()


if __name__ == '__main__':
    asyncio.run(main())
