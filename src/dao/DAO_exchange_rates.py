import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, aliased, selectinload

from src.exception.exceptions import CurrencyExchangeException, CurrencyException
from src.logging_config import setup_logging
from src.models import ExchangeRatesModel, CurrenciesModel
from src.routes.currencies import get_currency
from src.schemas.exchange_rates_schema import ExchangeRateSchema

setup_logging()

logger = logging.getLogger('logger')


class ExchangeDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_exchange_rates(self):
        try:
            query = (select(ExchangeRatesModel)
                     .options(joinedload(ExchangeRatesModel.base_currency),
                              joinedload(ExchangeRatesModel.target_currency)))
            result = await self.session.execute(query)
            return [ExchangeRateSchema.model_validate(exchange_rate) for exchange_rate in result.scalars().all()]
        except Exception as ex:
            logger.error(f"другая ошибка получения валюты, текст: {ex}")
            raise CurrencyExchangeException(status_code=500, message="База данных недоступна")

    async def get_exchange_rate(self, base_code, target_code):
        BaseCurrency = aliased(CurrenciesModel)
        TargetCurrency = aliased(CurrenciesModel)

        try:
            query = (select(ExchangeRatesModel)
                     .join(BaseCurrency, ExchangeRatesModel.base_currency)
                     .join(TargetCurrency, ExchangeRatesModel.target_currency)
                     .options(selectinload(ExchangeRatesModel.base_currency),
                              selectinload(ExchangeRatesModel.target_currency))
                     .where(BaseCurrency.code == base_code)
                     .where(TargetCurrency.code == target_code))
            result = await self.session.execute(query)
            logger.debug(f"Запрос на обменный курс валюта1={base_code}, валюта2={target_code}")
        except Exception as ex:
            logger.error(f"другая ошибка добавления валюты, текст: {ex}")
            raise CurrencyExchangeException(status_code=500, message="База данных недоступна")

        response_object = result.scalars().first()
        if response_object is None:
            raise CurrencyExchangeException(status_code=404, message="Обменный курс для пары не найден")
        response_model = ExchangeRateSchema.model_validate(response_object)
        return response_model

    async def create_exchange_rate(self, base_currency_code, target_currency_code, rate):
        if not all([base_currency_code, target_currency_code, rate]):
            logger.debug(f"Запрос на создание обменного курса без необходимых данных. "
                         f"base_currency_code={base_currency_code}, target_currency_code={target_currency_code}, "
                         f"rate={rate}")
            raise CurrencyExchangeException(status_code=400, message="Отсутствует нужное поле формы")
        try:
            base_currency = await get_currency(base_currency_code, db=self.session)
            target_currency = await get_currency(target_currency_code, db=self.session)
        except CurrencyException as ex:
            logger.debug(
                f"Запрос на получение валют при создании обменного курса. Ошибка получения одной из валют. Текст={ex}")
            raise CurrencyExchangeException(status_code=404,
                                            message="Одна (или обе) валюта из валютной пары не существует в БД")

        new_model = ExchangeRatesModel(
            base_currency_id=base_currency.id,
            target_currency_id=target_currency.id,
            rate=rate
        )
        self.session.add(new_model)
        logger.debug("добавлена модель в очередь")
        try:
            # Выполняем commit, чтобы сохранить данные
            await self.session.commit()
            logger.debug("коммит")

            # Обновляем модель с подгруженными внешними ключами
            await self.session.refresh(new_model, with_for_update=False)

            # Подгружаем связанные модели (base_currency и target_currency). Можно было делать через запрос
            await self.session.refresh(new_model, attribute_names=["base_currency", "target_currency"])

            return ExchangeRateSchema.model_validate(new_model)  # Используем модель для валидации данных
        except IntegrityError as ex:
            logger.debug(f"Запрос на создание курса который уже существует. Текст {ex}")
            raise CurrencyExchangeException(status_code=409, message="Валютная пара с таким кодом уже существует")

        except Exception as ex:
            logger.error(f"другая ошибка добавления валюты, текст: {ex}")
            raise CurrencyExchangeException(status_code=500, message="База данных недоступна")

    async def update_exchange_rate(self, base_code, target_code, new_rate):

        if len(base_code + target_code) != 6 or not new_rate:
            logger.debug(f"Запрос на изменение обменного курса без нужных полей. "
                         f"base_code={base_code}, target_code={target_code}, new_rate={new_rate}")
            raise CurrencyExchangeException(status_code=400, message="Отсутствует нужное поле формы")

        try:
            result = await self.session.execute(
                select(ExchangeRatesModel).where(
                    ExchangeRatesModel.base_currency.has(CurrenciesModel.code == base_code))
                .where(ExchangeRatesModel.target_currency.has(CurrenciesModel.code == target_code)))
            logger.debug(f"запрос на поиск обменного курса с параметрами {base_code}-{target_code}")
        except Exception as ex:
            logger.error(f"другая ошибка при запросе на получение обменного курса, текст: {ex}")
            raise CurrencyExchangeException(status_code=500, message="База данных недоступна")

        old_model = result.scalars().first()

        if old_model is None:
            logger.debug(f"Поиск обменного курса {base_code}-{target_code}. Такого курса нет")
            raise CurrencyExchangeException(status_code=404, message="Валютная пара отсутствует в базе данных")

        try:
            # изменение курса в полученной модели
            old_model.rate = new_rate
            await self.session.commit()  # Сохраняем изменения в базе данных

            # Подгружаем связанные модели (base_currency и target_currency). Можно было делать через запрос
            await self.session.refresh(old_model, attribute_names=["base_currency", "target_currency"])
            logger.debug("обменный курс модели обновлен")
        except Exception as ex:
            logger.error(f"другая ошибка при сохранении м обновлении обменного курса, текст: {ex}")
            raise CurrencyExchangeException(status_code=500, message="База данных недоступна")

        return ExchangeRateSchema.model_validate(old_model)  # Возвращаем обновленный объект в формате схемы
