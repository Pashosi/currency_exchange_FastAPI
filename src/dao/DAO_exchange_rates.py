import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, relationship, aliased, selectinload

from src.logging_config import setup_logging
from src.models import ExchangeRatesModel, CurrenciesModel
from src.routes.currencies import get_currency
from src.routes import exchange_rates
from src.schemas.exchange_schema import ExchangeRateSchema

setup_logging()

logger = logging.getLogger('logger')

class ExchangeDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_exchange_rates(self):
        result = await self.session.execute(
            select(ExchangeRatesModel)
            .options(joinedload(ExchangeRatesModel.base_currency), joinedload(ExchangeRatesModel.target_currency)))
        return [ExchangeRateSchema.model_validate(exchange_rate) for exchange_rate in result.scalars().all()]

    async def get_exchange_rate(self, base_code, target_code):
        logger.debug(f"Тип сессии: {type(self.session)}")
        BaseCurrency = aliased(CurrenciesModel)
        TargetCurrency = aliased(CurrenciesModel)

        stmt = (select(ExchangeRatesModel)
                .join(BaseCurrency, ExchangeRatesModel.base_currency)
                .join(TargetCurrency, ExchangeRatesModel.target_currency)
                .options(selectinload(ExchangeRatesModel.base_currency), selectinload(ExchangeRatesModel.target_currency))
                .where(BaseCurrency.code == base_code)
                .where(TargetCurrency.code == target_code))
        logger.debug(f"Тип сессии: {type(self.session)}")
        result = await self.session.execute(stmt)
        logger.debug(f"Получен обменный курс валюта1={base_code}, валюта2={target_code}")
        return ExchangeRateSchema.model_validate(result.scalars().first())

    async def create_exchange_rate(self, base_currency_code, target_currency_code, rate):
        base_currency = await get_currency(base_currency_code, db=self.session)
        target_currency = await get_currency(target_currency_code, db=self.session)
        new_model = ExchangeRatesModel(
            base_currency_id = base_currency.id,
            target_currency_id=target_currency.id,
            rate=rate
        )
        self.session.add(new_model)
        logger.debug("добавлена модель")
        try:
            # Выполняем commit, чтобы сохранить данные
            await self.session.commit()
            logger.debug("коммит")

            # Обновляем модель с подгруженными внешними ключами
            await self.session.refresh(new_model, with_for_update=False)

            # Подгружаем связанные модели (base_currency и target_currency). Можно было делать через запрос
            await self.session.refresh(new_model, attribute_names=["base_currency", "target_currency"])

            return ExchangeRateSchema.model_validate(new_model)  # Используем модель для валидации данных
        except Exception as ex:
            logger.error(f"другая ошибка добавления валюты, текст: {ex}")
            return {"message": str(ex)}

    async def update_exchange_rate(self, base_code, target_code, new_rate):
        result = await self.session.execute(select(ExchangeRatesModel).where(ExchangeRatesModel.base_currency.has(CurrenciesModel.code == base_code))
                .where(ExchangeRatesModel.target_currency.has(CurrenciesModel.code == target_code)))
        logger.debug(f"запрос на поиск обменного курса с параметрами {base_code}-{target_code}")
        old_model = result.scalars().first()

        # изменение курса в полученной модели
        old_model.rate = new_rate
        await self.session.commit()  # Сохраняем изменения в базе данных

        # Подгружаем связанные модели (base_currency и target_currency). Можно было делать через запрос
        await self.session.refresh(old_model, attribute_names=["base_currency", "target_currency"])
        logger.debug("обменный курс модели обновлен")

        return ExchangeRateSchema.model_validate(old_model)  # Возвращаем обновленный объект в формате схемы
