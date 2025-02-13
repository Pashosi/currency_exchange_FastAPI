"""empty message

Revision ID: 964377800b21
Revises: 
Create Date: 2025-02-10 07:24:31.045725

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "964377800b21"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "currencies",
        sa.Column("code", sa.String(length=3), nullable=False),
        sa.Column("full_name", sa.String(length=50), nullable=False),
        sa.Column("sign", sa.String(length=3), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_currencies_code"), "currencies", ["code"], unique=True
    )
    op.create_table(
        "exchange_rates",
        sa.Column("base_currency_id", sa.Integer(), nullable=False),
        sa.Column("target_currency_id", sa.Integer(), nullable=False),
        sa.Column("rate", sa.DECIMAL(precision=9, scale=6), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["base_currency_id"], ["currencies.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["target_currency_id"], ["currencies.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "base_currency_id", "target_currency_id", name="unique_currency_id"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("exchange_rates")
    op.drop_index(op.f("ix_currencies_code"), table_name="currencies")
    op.drop_table("currencies")
    # ### end Alembic commands ###
