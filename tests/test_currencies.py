import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from src.schemas.currency_schema import CurrencySchema


class TestCurrencies:

    @pytest.mark.asyncio(loop_scope='session')
    async def test_get_currencies(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.get("/currencies")
            assert response.status_code == 200
            print(response.json())
            CurrencySchema.model_validate(response.json()[0])

    @pytest.mark.asyncio(loop_scope='session')
    async def test_add_currency_409(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.post(
                "/currencies",
                data={
                    "name": "UnitedStatesDollar",
                    "code": "USD",
                    "sign": "$",
                }
            )
            assert response.status_code == 409
            assert response.json() == {"message": "Валюта с таким кодом уже существует"}

    @pytest.mark.parametrize(
        "data, code",
        [
            ({"name": "UnitedDollar", "code": "UUUUU", "sign": "#"}, 422),
            ({"name": "UnitedDollar" * 4, "code": "UU", "sign": "####"}, 422),
            ({"name": "UnitedDollar", "code": "UU"}, 400),
            ({"name": "UnitedDollar", "sign": "#"}, 400),
            ({"code": "UU", "sign": "#"}, 400),
        ]
    )
    @pytest.mark.asyncio(loop_scope="session")
    async def test_add_currency_required_field_missing(self, data, code):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.post(
                "/currencies",
                data=data
            )
            assert response.status_code == code

    @pytest.mark.asyncio(loop_scope="session")
    async def test_add_currency(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            currencies = await client.get("/currencies")
            response = await client.post(
                "/currencies",
                data={
                    "name": "BritishPound",
                    "code": "GBP",
                    "sign": "£"
                }
            )
            assert response.status_code == 201
            assert len(currencies.json()) != len(response.json())
            CurrencySchema.model_validate(response.json())

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_currency_usd(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.get('/currency/USD')
            assert response.status_code == 200
            assert response.json()["code"] == "USD"
            CurrencySchema.model_validate(response.json())

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_currency_without_code(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.get('/currency')
            assert response.status_code == 400
            assert response.json() == {'message': 'Код валюты отсутствует в адресе'}

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_currency_not_found(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.get('/currency/UUU')
            assert response.status_code == 404
            assert response.json() == {'message': "Валюта не найдена"}
            response = await client.get('/currency/UU')
            assert response.status_code == 422

# class TestExchangeRates:
#
#     @pytest.mark.asyncio(loop_scope="module")
#     async def test_exchange_rates(self, test_db):
#         async with AsyncClient(
#                 transport=ASGITransport(app=app),
#                 base_url="http://test",
#         ) as client:
#             response = await client.get("/exchangeRates")
#             assert response.status_code == 200
#             print(response.json())
#             ExchangeRateSchema.model_validate(response.json()[0])
#
#     @pytest.mark.asyncio(loop_scope="module")
#     async def test_exchange_ratess(self, test_db):
#         async with AsyncClient(
#                 transport=ASGITransport(app=app),
#                 base_url="http://test",
#         ) as client:
#             response = await client.get("/exchangeRates")
#             assert response.status_code == 200
#             print(response.json())
#             ExchangeRateSchema.model_validate(response.json()[0])
