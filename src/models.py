from sqlalchemy import String, ForeignKey, DECIMAL
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column


class Base(AsyncAttrs, DeclarativeBase):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class CurrenciesModel(Base):
    __tablename__ = "currencies"

    code: Mapped[str] = mapped_column(String(3), index=True, unique=True)
    full_name: Mapped[str] = mapped_column(String(50))
    sign: Mapped[str] = mapped_column(String(3))

class ExchangeRatesModel(Base):
    __tablename__ = "exchange_rates"

    base_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id", ondelete='CASCADE'))
    target_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id", ondelete='CASCADE'))
    rate: Mapped[DECIMAL] = mapped_column(DECIMAL(precision=6, scale=6))
