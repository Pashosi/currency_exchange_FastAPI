import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from main import app
from src.config import settings
from src.dao.DAO_currency import CurrencyDAO
from src.dao.DAO_exchange_rates import ExchangeDAO
from src.database import get_db
from src.models import Base

engine_test = create_async_engine(url=settings.TEST_DATABASE_URL, echo=False)

session_test = async_sessionmaker(bind=engine_test)

list_currencies = [
    {"full_name": "UnitedStatesDollar", "code": "USD", "sign": "$"},  # Доллар США
    {"full_name": "Euro", "code": "EUR", "sign": "€"},  # Евро
    {"full_name": "JapaneseYen", "code": "JPY", "sign": "¥"},  # Японская иена
]

exchange_rates = [
    {"base_currency": "USD", "target_currency": "EUR", "rate": 0.92},
    {"base_currency": "USD", "target_currency": "JPY", "rate": 150.0},
    {"base_currency": "JPY", "target_currency": "USD", "rate": 0.0067},
]


async def add_currencies(session):
    dao = CurrencyDAO(session)
    try:
        for currency in list_currencies:
            await dao.create_currency(full_name=currency["full_name"], code=currency["code"], sign=currency["sign"])
    except Exception as e:
        print(f"Базовые валюты уже добавлены, текст:{e}")


async def add_exchange_rates(session):
    dao = ExchangeDAO(session)
    try:
        for exchange_rate in exchange_rates:
            await dao.create_exchange_rate(
                base_currency_code=exchange_rate["base_currency"],
                target_currency_code=exchange_rate["target_currency"],
                rate=exchange_rate["rate"]
            )
    except Exception as e:
        print(f"Базовые обменные курсы уже добавлены, текст:{e}")


@pytest.fixture(scope="function", autouse=True)
async def test_db():
    # Сначала создаем таблицы
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Создаем сессию
    async with session_test() as sess:
        await add_currencies(sess)  # Добавление валют
        await add_exchange_rates(sess)
        yield sess  # возвращение сессии следующему тесту

    # Удаляем таблицы после теста
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_db():
    async with session_test() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db
