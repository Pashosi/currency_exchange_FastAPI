from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.DAO_exchange_rates import ExchangeDAO
from src.database import get_db
from src.models import CurrenciesModel
from src.schemas.currency_schema import CurrencySchema
from src.schemas.exchange_rates_schema import ExchangeRateSchema

router = APIRouter(tags=["Обменные курсы"])


@router.get("/exchangeRates", status_code=200)
async def get_exchange_rates(db: AsyncSession = Depends(get_db)) -> list[ExchangeRateSchema]:
    dao_exchange = ExchangeDAO(db)
    result = await dao_exchange.get_exchange_rates()
    return result


@router.get("/exchangeRate/{codes}", status_code=200)
async def get_exchange_rate(
        codes: Annotated[str, Path(max_length=6, min_length=6, pattern="^[A-Z]{6}$")],
        db: AsyncSession = Depends(get_db)
) -> ExchangeRateSchema:
    base_code = codes[:3]
    target_code = codes[3:]
    dao_exchange = ExchangeDAO(db)

    result = await dao_exchange.get_exchange_rate(base_code=base_code, target_code=target_code)
    return result


@router.post("/exchangeRates", status_code=201)
async def create_exchange_rate(
        base_currency_code: Annotated[str, Query(max_length=3, min_length=3, pattern="^[A-Z]{3}$")],
        target_currency_code: Annotated[str, Query(max_length=3, min_length=3, pattern="^[A-Z]{3}$")],
        rate: float,
        db: AsyncSession = Depends(get_db)
) -> ExchangeRateSchema:
    dao_exchange = ExchangeDAO(db)

    result = await dao_exchange.create_exchange_rate(base_currency_code=base_currency_code,
                                                     target_currency_code=target_currency_code, rate=rate)
    return result

@router.patch("/exchangeRate/{codes}", status_code=200)
async def update_exchange_rate(
        new_rate: Annotated[float, Query(ge=0)],
        codes: Annotated[str, Path(max_length=6, min_length=6, pattern="^[A-Z]{6}$")],
        db: AsyncSession = Depends(get_db),
) -> ExchangeRateSchema:
    base_code = codes[:3]
    target_code = codes[3:]
    dao_exchange = ExchangeDAO(db)

    result = await dao_exchange.update_exchange_rate(base_code=base_code, target_code=target_code, new_rate=new_rate)
    return result