"""initial migration

Revision ID: c7ec61ae64ae
Revises:
Create Date: 2025-06-25 18:51:47.883829

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c7ec61ae64ae"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "hotels",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("hotels")
