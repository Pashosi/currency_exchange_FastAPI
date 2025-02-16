import pytest
from httpx import AsyncClient, ASGITransport

from main import app
from src.schemas.exchange_schema import ExchangeSchema


class TestExample:
    @pytest.mark.asyncio(loop_scope='session')
    async def test_get_direct_exchange(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            parameters = {'from': 'USD', 'to': 'EUR', 'amount': '3'}
            response = await client.get("/exchange", params=parameters)
            assert response.status_code == 200
            ExchangeSchema.model_validate(response.json())

    @pytest.mark.asyncio(loop_scope='session')
    async def test_get_reverse_exchange(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            parameters = {'from': 'EUR', 'to': 'USD', 'amount': '3'}
            response = await client.get("/exchange", params=parameters)
            assert response.status_code == 200
            ExchangeSchema.model_validate(response.json())

    @pytest.mark.asyncio(loop_scope='session')
    async def test_get_cross_exchange(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            parameters = {'from': 'JPY', 'to': 'EUR', 'amount': '3'}
            response = await client.get("/exchange", params=parameters)
            assert response.status_code == 200
            ExchangeSchema.model_validate(response.json())

    @pytest.mark.asyncio(loop_scope='session')
    async def test_convert_same_currency(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            parameters = {'from': 'USD', 'to': 'USD', 'amount': '100'}
            response = await client.get("/exchange", params=parameters)
            assert response.status_code == 200
            data = response.json()
            ExchangeSchema.model_validate(data)
            assert data['amount'] == '100.0'
            assert data['rate'] == '100.0'
            assert data['convertedAmount'] == '1'

    @pytest.mark.asyncio(loop_scope='session')
    async def test_get_exchange_field_missing(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            parameters = {'from': 'JPY', 'to': 'EUR'}
            response = await client.get("/exchange", params=parameters)
            assert response.status_code == 400
            assert response.json() == {"message": "Отсутствует нужное поле формы"}

    @pytest.mark.asyncio(loop_scope='session')
    async def test_get_exchange_not_found(self):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            parameters = {'from': 'JPY', 'to': 'DDD', 'amount': '100'}
            response = await client.get("/exchange", params=parameters)
            assert response.status_code == 404
            assert response.json() == {"message": "Обменный курс не найден"}
