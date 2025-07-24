"""user_email = unique

Revision ID: 4249a4ec478b
Revises: 708180d7c3c6
Create Date: 2025-06-28 13:49:31.542275

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "4249a4ec478b"
down_revision: Union[str, Sequence[str], None] = "708180d7c3c6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("users", "phone", existing_type=sa.VARCHAR(length=20), nullable=True)
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
    op.alter_column("users", "phone", existing_type=sa.VARCHAR(length=20), nullable=True)
