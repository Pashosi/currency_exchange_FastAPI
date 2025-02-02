from sqlalchemy import String, ForeignKey, DECIMAL, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy.orm import mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class CurrenciesModel(Base):
    __tablename__ = "currencies"

    code: Mapped[str] = mapped_column(String(3), index=True, unique=True)
    full_name: Mapped[str] = mapped_column(String(50))
    sign: Mapped[str] = mapped_column(String(3))

    def __repr__(self):
        return f'CurrenciesModel: (code = {self.code}, full_name = {self.full_name}, sign = {self.sign})'


class ExchangeRatesModel(Base):
    __tablename__ = "exchange_rates"
    __table_args__ = (
        UniqueConstraint('base_currency_id', 'target_currency_id', name='unique_currency_id'),  # Уникальный набор полей
    )

    base_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id", ondelete='CASCADE'))
    target_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id", ondelete='CASCADE'))
    rate: Mapped[DECIMAL] = mapped_column(DECIMAL(precision=9, scale=6))

    # Определяем отношения
    base_currency: Mapped["CurrenciesModel"] = relationship(
        "CurrenciesModel", foreign_keys='ExchangeRatesModel.base_currency_id'
    )
    target_currency: Mapped["CurrenciesModel"] = relationship(
        "CurrenciesModel", foreign_keys='ExchangeRatesModel.target_currency_id'
    )

    def __repr__(self):
        return (f'ExchangeRatesModel: (id = {self.id}, base_currency_id = {self.base_currency_id}, '
                f'target_currency_id = {self.target_currency_id}, rate = {self.rate})')
