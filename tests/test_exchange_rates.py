import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from src.schemas.exchange_rates_schema import ExchangeRateSchema


class TestExchangeRates:

    @pytest.mark.asyncio(loop_scope='session')
    async def test_exchange_rates(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.get("/exchangeRates")
            assert response.status_code == 200
            response_json = response.json()
            assert isinstance(response_json, list)
            for rate in response_json:
                ExchangeRateSchema.model_validate(rate)

    @pytest.mark.asyncio(loop_scope='session')
    async def test_exchange_rate_usd(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.get("/exchangeRate/USDEUR")
            assert response.status_code == 200
            ExchangeRateSchema.model_validate(response.json())

    @pytest.mark.asyncio(loop_scope='session')
    async def test_exchange_rate_required_field_missing(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.get("/exchangeRate")
            assert response.status_code == 400
            assert response.json() == {"message": "Коды валют пары отсутствуют в адресе"}

    @pytest.mark.parametrize(
        "codes, response_code",
        [
            ("USDDDDd", 422),
            ("USDeur", 422),
            ("usdeur", 422),
            ("usdeurs", 422),
            ("USDEURR", 422),
        ]
    )
    @pytest.mark.asyncio(loop_scope='session')
    async def test_get_exchange_rate_incorrect_input(self, codes, response_code):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.get(f"/exchangeRate/{codes}")
            assert response.status_code == response_code

    @pytest.mark.asyncio(loop_scope='session')
    async def test_exchange_rate_not_found(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.get("/exchangeRate/USDDDD")
            assert response.status_code == 404
            assert response.json() == {"message": "Обменный курс для пары не найден"}

    @pytest.mark.asyncio(loop_scope='session')
    async def test_update_exchange_rate_required_field_missing(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.patch("/exchangeRate/USDEUR")
            assert response.status_code == 400
            assert response.json() == {"message": "Отсутствует нужное поле формы"}

    @pytest.mark.asyncio(loop_scope='session')
    async def test_update_exchange_rate_not_found(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.patch("/exchangeRate/USDDDD", data={"rate": 0.99})
            assert response.status_code == 404
            assert response.json() == {"message": "Валютная пара отсутствует в базе данных"}

    @pytest.mark.asyncio(loop_scope='session')
    async def test_update_exchange_rate_successfully(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.patch("/exchangeRate/USDEUR", data={"rate": 0.99})
            assert response.status_code == 200
            ExchangeRateSchema.model_validate(response.json())

    @pytest.mark.asyncio(loop_scope='session')
    async def test_create_exchange_rate_successfully(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.post(
                "/exchangeRates",
                data={
                    "baseCurrencyCode": "JPY",
                    "targetCurrencyCode": "EUR",
                    "rate": 0.99
                })
            assert response.status_code == 201
            ExchangeRateSchema.model_validate(response.json())

    @pytest.mark.asyncio(loop_scope='session')
    async def test_create_exchange_rate_currency_not_exist(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.post(
                "/exchangeRates",
                data={
                    "baseCurrencyCode": "JPY",
                    "targetCurrencyCode": "EEE",
                    "rate": 0.99
                })
            assert response.status_code == 404
            assert response.json() == {"message": "Одна (или обе) валюта из валютной пары не существует в БД"}

    @pytest.mark.asyncio(loop_scope='session')
    async def test_create_exchange_rate_currency_already_exist(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.post(
                "/exchangeRates",
                data={
                    "baseCurrencyCode": "USD",
                    "targetCurrencyCode": "EUR",
                    "rate": 0.99
                })
            assert response.status_code == 409
            assert response.json() == {"message": "Валютная пара с таким кодом уже существует"}

    @pytest.mark.asyncio(loop_scope='session')
    async def test_create_exchange_rate_field_missing(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.post(
                "/exchangeRates",
                data={
                    "baseCurrencyCode": "USD",
                    "targetCurrencyCode": "EUR",
                })
            assert response.status_code == 400
            assert response.json() == {"message": "Отсутствует нужное поле формы"}
