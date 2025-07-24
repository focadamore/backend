"""rooms migration

Revision ID: 62664a0019df
Revises: c7ec61ae64ae
Create Date: 2025-06-25 21:01:08.297065

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "62664a0019df"
down_revision: Union[str, Sequence[str], None] = "c7ec61ae64ae"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["hotel_id"], ["hotels.id"], name="fk_rooms_hotels_id"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("rooms")
