"""users add phone

Revision ID: 708180d7c3c6
Revises: ef2fbd23c75e
Create Date: 2025-06-28 11:44:55.266247

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "708180d7c3c6"
down_revision: Union[str, Sequence[str], None] = "ef2fbd23c75e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("phone", sa.String(length=20), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "phone")
