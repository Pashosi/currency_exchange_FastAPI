from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.services.exchange_service import ExchangeService

router = APIRouter(tags=["Конвертрация валют"])


@router.get("/exchange", status_code=200)
async def get_exchange(
        amount: Annotated[float | None, Query(ge=0)] = None,
        base_currency: Annotated[str, Query(alias="from")] = None,
        target_currency: Annotated[str, Query(alias="to")] = None,
        db: AsyncSession = Depends(get_db),
):
    service = ExchangeService(db)
    result = await service.currencies_conversion(
        base_currency=base_currency,
        target_currency=target_currency,
        amount=amount
    )
    return result
