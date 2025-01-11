from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.DAO_currency import CurrencyDAO
from src.database import get_db
from src.schemas.currency_schema import CurrencySchema

router = APIRouter(tags=["Валюты"])

@router.get('/currencies')
async def get_currencies(db : AsyncSession = Depends(get_db)) -> list[CurrencySchema]:
    dao_currency = CurrencyDAO(db)
    result = await dao_currency.get_currencies()
    return result


@router.post('/currencies')
async def add_currency(currency: CurrencySchema, db : AsyncSession = Depends(get_db)):
    dao_currency = CurrencyDAO(db)

    curr = await dao_currency.create_currency(currency=currency)
    return curr


@router.get('/currency/{code}')
async def get_currency(code: str, db : AsyncSession = Depends(get_db)):
    dao_currency = CurrencyDAO(db)
    result = await dao_currency.get_currency(code=code)
    return result