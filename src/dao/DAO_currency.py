import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.exception.exceptions import CurrencyException
from src.logging_config import setup_logging
from src.models import CurrenciesModel
from src.schemas.currency_schema import CurrencySchemaOut

setup_logging()

logger = logging.getLogger('logger')


class CurrencyDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_currency(self, code: str):
        try:
            result = await self.session.execute(select(CurrenciesModel).where(CurrenciesModel.code == code))
            result = result.scalars().first()
        except Exception as ex:
            logger.error(f"Ошибка при запросе на получении валюты {code} message={ex}")
            raise CurrencyException(status_code=500, message="Ошибка доступа в базу данных")

        if result is None:
            logger.debug(f"Не найдена валюта {code}")
            raise CurrencyException(status_code=404, message="Валюта не найдена")

        return result

    async def create_currency(self, code: str, full_name: str, sign: str) -> CurrencySchemaOut:
        if not all([code, full_name, sign]) or len(full_name) < 3:
            logger.debug(f"Отсутствует поле: code={code} name={full_name} sign={sign}")
            raise CurrencyException(status_code=400, message="Отсутствует нужное поле формы")

        new_model = CurrenciesModel(
            code=code,
            full_name=full_name,
            sign=sign
        )
        self.session.add(new_model)
        logger.debug(f"модель валюты {code} добавлена в ожидание")
        try:
            # Выполняем commit, чтобы сохранить данные
            await self.session.commit()
            logger.debug(f"коммит модели валюты {code} в БД")

            # Обновление модели
            await self.session.refresh(new_model)  # Это гарантирует, что все атрибуты обновлены из базы данных
            logger.debug(f"обновление валюты {code} из БД")
            return CurrencySchemaOut.model_validate(new_model)  # Используем модель для валидации данных

        except IntegrityError as ex:
            logger.debug(f"код валюты уже есть. текст ошибки: {ex}")
            raise CurrencyException(status_code=409, message="Валюта с таким кодом уже существует")
        except Exception as ex:
            logger.error(f"другая ошибка добавления валюты, текст: {ex}")
            raise CurrencyException(status_code=500, message="база данных недоступна")

    async def get_currencies(self) -> list[CurrencySchemaOut]:
        try:
            result = await self.session.execute(select(CurrenciesModel))
            list_schemas = [CurrencySchemaOut.model_validate(currency) for currency in result.scalars().all()]
            return list_schemas
        except Exception as ex:
            logger.error(f"Ошибка при запросе на получении списка валют message={ex}")
            raise CurrencyException(status_code=500, message="Ошибка доступа в базу данных")
