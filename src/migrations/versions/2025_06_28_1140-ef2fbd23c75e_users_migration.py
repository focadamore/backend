"""users migration

Revision ID: ef2fbd23c75e
Revises: 62664a0019df
Create Date: 2025-06-28 11:40:57.174513

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ef2fbd23c75e"
down_revision: Union[str, Sequence[str], None] = "62664a0019df"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
