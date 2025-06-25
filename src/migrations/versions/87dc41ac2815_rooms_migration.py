"""rooms migration

Revision ID: 87dc41ac2815
Revises: c7ec61ae64ae
Create Date: 2025-06-25 20:00:28.943159

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87dc41ac2815'
down_revision: Union[str, Sequence[str], None] = 'c7ec61ae64ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('rooms',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('hotel_id', sa.Integer(), nullable=False, ),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('price', sa.Integer(), nullable=False),
                    sa.Column('quantity', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], name="fk_rooms_hotel_id")
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('rooms')
