import logging
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP

from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.DAO_exchange_rates import ExchangeDAO
from src.exception.exceptions import CurrencyExchangeException
from src.logging_config import setup_logging
from src.schemas.exchange_schema import ExchangeSchemaOut

setup_logging()

logger = logging.getLogger('logger')


class ExchangeService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def currencies_conversion(self, base_currency, target_currency, amount):
        dao_exchange = ExchangeDAO(self.session)
        if amount is None:
            logger.debug("Не ввел amount")
            raise CurrencyExchangeException(status_code=400, message="Отсутствует нужное поле формы")
        try:
            # Прямой курс
            rate = await dao_exchange.get_exchange_rate(base_currency, target_currency)
            converted = (Decimal(rate.rate) * Decimal(amount)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
            logger.debug(f"Конвертация валюты с {base_currency} на {target_currency} по прямому курсу")

            return ExchangeSchemaOut(
                base_currency=rate.base_currency,
                target_currency=rate.target_currency,
                rate=rate.rate.normalize(),
                amount=amount,
                converted_amount=converted
            )

        except CurrencyExchangeException:
            try:
                # Обратный курс
                rate = await dao_exchange.get_exchange_rate(target_currency, base_currency)
                calculate_rate = (Decimal('1') / Decimal(rate.rate)).quantize(Decimal('.00001'), rounding=ROUND_HALF_UP)
                logger.debug(f'Обратный обменный курс calculate_rate={calculate_rate}')
                converted = (Decimal(calculate_rate) * Decimal(amount)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
                logger.debug(f"Конвертация валюты с {base_currency} на {target_currency} по обратному курсу")

                return ExchangeSchemaOut(
                    base_currency=rate.base_currency,
                    target_currency=rate.target_currency,
                    rate=calculate_rate.normalize(),
                    amount=amount,
                    converted_amount=converted
                )

            except CurrencyExchangeException:
                try:
                    # Кросс-курс через USD
                    base_rate_usd = await dao_exchange.get_exchange_rate("USD", base_currency)
                    target_rate_usd = await dao_exchange.get_exchange_rate("USD", target_currency)
                    logger.debug(f"Кросс-курс. Запросы на получение "
                                 f"курсов с долларом {base_currency} и {target_currency}")

                    rate = (Decimal(base_rate_usd.rate) * Decimal(target_rate_usd.rate)).quantize(
                        Decimal('.00001'), rounding=ROUND_HALF_UP
                    )
                    converted = (Decimal(rate) * Decimal(amount)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

                    return ExchangeSchemaOut(
                        base_currency=base_rate_usd.target_currency,
                        target_currency=target_rate_usd.target_currency,
                        rate=rate.normalize(),
                        amount=amount,
                        converted_amount=converted
                    )

                except CurrencyExchangeException:
                    logger.debug("Обменный курс не найден")
                    raise CurrencyExchangeException(status_code=404, message="Обменный курс не найден")
