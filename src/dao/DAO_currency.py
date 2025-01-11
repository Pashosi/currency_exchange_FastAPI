import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.logging_config import setup_logging
from src.models import CurrenciesModel
from src.schemas.currency_schema import CurrencySchema

setup_logging()

logger = logging.getLogger('logger')


class CurrencyDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_currency(self, code: str):
        try:
            result = await self.session.execute(select(CurrenciesModel).where(CurrenciesModel.code == code))
            result = result.scalars().first()
        # TODO обработка не правильного кода, когда выводится null
        except Exception as ex:
            return {"message": f"Ошибка получения валюты: {ex}"}

        return result

    async def create_currency(self, currency: CurrencySchema):
        new_model = CurrenciesModel(
            code=currency.code,
            full_name=currency.full_name,
            sign=currency.sign
        )
        self.session.add(new_model)
        logger.debug("добавлена модель")
        try:
            # Выполняем commit, чтобы сохранить данные
            await self.session.commit()
            logger.debug("коммит")

            # Обновление модели
            await self.session.refresh(new_model)  # Это гарантирует, что все атрибуты обновлены из базы данных
            logger.debug(new_model)
            return CurrencySchema.model_validate(new_model)  # Используем модель для валидации данных

        except IntegrityError as ex:
            logger.info(f"код валюты не уникален. текст ошибки: {ex}")
            return {"message": "Currency code must be unique"}
        except Exception as ex:
            logger.error(f"другая ошибка добавления валюты, текст: {ex}")
            return {"message": str(ex)}

    async def get_currencies(self):
        result = await self.session.execute(select(CurrenciesModel))
        return [CurrencySchema.model_validate(currency) for currency in result.scalars().all()]