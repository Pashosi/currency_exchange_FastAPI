import logging
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from logging import Logger

from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.DAO_exchange_rates import ExchangeDAO
from src.logging_config import setup_logging
from src.schemas.exchange_schema import ExchangeSchema

setup_logging()

logger = logging.getLogger('logger')


class ExchangeService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def currencies_conversion(self, base_currency, target_currency, amount):
        # Прямой курс
        dao_exchange = ExchangeDAO(self.session)
        if rate := await dao_exchange.get_exchange_rate(base_currency, target_currency):
            converted = (Decimal(rate.rate) * Decimal(amount)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
            logger.debug(f"Конвертация валюты с {base_currency} на {target_currency} по прямому курсу")
            result = ExchangeSchema(
                base_currency=rate.base_currency,
                target_currency=rate.target_currency,
                rate=rate.rate.normalize(),
                amount=amount,
                converted_amount=converted
            )

            return result
        # Обратный курс
        elif rate := await dao_exchange.get_exchange_rate(target_currency, base_currency):
            calculate_rate = (Decimal('1') / Decimal(rate.rate)).quantize(Decimal('.00001'), rounding=ROUND_HALF_UP)
            logger.debug(f'обратный обменный курс calculate_rate={calculate_rate}')
            converted = (Decimal(calculate_rate) * Decimal(amount)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
            logger.debug(f"Конвертация валюты с {base_currency} на {target_currency} по обратному курсу")
            result = ExchangeSchema(
                base_currency=rate.base_currency,
                target_currency=rate.target_currency,
                rate=calculate_rate.normalize(),
                amount=amount,
                converted_amount=converted
            )
            return result

        # Кросс-курс
        elif await dao_exchange.get_exchange_rate("USD", base_currency) and await dao_exchange.get_exchange_rate("USD",
                                                                                                                target_currency):
            base_rate_usd = await dao_exchange.get_exchange_rate("USD", base_currency)
            target_rate_usd = await dao_exchange.get_exchange_rate("USD",target_currency)
            logger.debug(f"Кросс-курс. Запросы на получение курсов с долларом {base_currency} и {target_currency}")
            rate = (Decimal(base_rate_usd.rate) * Decimal(target_rate_usd.rate)).quantize(Decimal('.00001'),
                                                                                         rounding=ROUND_HALF_UP)
            converted = (Decimal(rate) * Decimal(amount)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

            result = ExchangeSchema(
                base_currency=base_rate_usd.target_currency,
                target_currency=target_rate_usd.target_currency,
                rate=rate.normalize(),
                amount=amount,
                converted_amount=converted
            )
            return result
        