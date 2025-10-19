"""add_hospital_id_to_items

Revision ID: 440f80f35c44
Revises: 1fcf288d2b1f
Create Date: 2025-10-19 06:07:22.104892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '440f80f35c44'
down_revision: Union[str, Sequence[str], None] = '1fcf288d2b1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add hospital_id column to items table
    op.add_column('items', sa.Column('hospital_id', sa.Integer(), nullable=False, server_default='1'))
    op.create_index(op.f('ix_items_hospital_id'), 'items', ['hospital_id'], unique=False)
    op.create_foreign_key(op.f('items_hospital_id_fkey'), 'items', 'hospitals', ['hospital_id'], ['id'], ondelete='RESTRICT')

    # Remove server_default after adding the column
    op.alter_column('items', 'hospital_id', server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    # Remove foreign key and index
    op.drop_constraint(op.f('items_hospital_id_fkey'), 'items', type_='foreignkey')
    op.drop_index(op.f('ix_items_hospital_id'), table_name='items')
    op.drop_column('items', 'hospital_id')
