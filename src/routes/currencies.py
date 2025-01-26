from typing import Annotated

from fastapi import APIRouter, Depends, Query, Path, HTTPException, Body, Form
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.DAO_currency import CurrencyDAO
from src.database import get_db
from src.exception.exceptions import CurrencyException
from src.schemas.currency_schema import CurrencySchema

router = APIRouter(tags=["Валюты"])


@router.get('/currencies', status_code=200)
async def get_currencies(db: AsyncSession = Depends(get_db)) -> list[CurrencySchema]:
    dao_currency = CurrencyDAO(db)
    result = await dao_currency.get_currencies()
    return result


@router.post('/currencies', status_code=201)
async def add_currency(
        code: Annotated[str, Form()] = '',
        name: Annotated[str, Form()] = '',
        sign: Annotated[str, Form()] = '',
        db: AsyncSession = Depends(get_db),
):
    dao_currency = CurrencyDAO(db)

    curr = await dao_currency.create_currency(code=code, full_name=name, sign=sign)
    return curr


@router.get('/currency/{code}', status_code=200)
async def get_currency(code: Annotated[str, Path(max_length=3, min_length=3, pattern="^[A-Z]{3}$")],
                       db: AsyncSession = Depends(get_db)) -> CurrencySchema:
    dao_currency = CurrencyDAO(db)
    result = await dao_currency.get_currency(code=code)
    return CurrencySchema.model_validate(result)


@router.get('/currency')
async def get_currency_without_code(db: AsyncSession = Depends(get_db)):
    raise CurrencyException(status_code=400, message=f"Код валюты отсутствует в адресе")
