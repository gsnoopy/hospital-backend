"""add_hospital_id_to_categories_and_subcategories

Revision ID: ee5722e6062d
Revises: 440f80f35c44
Create Date: 2025-10-19 06:13:32.046829

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee5722e6062d'
down_revision: Union[str, Sequence[str], None] = '440f80f35c44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add hospital_id column to categories table
    op.add_column('categories', sa.Column('hospital_id', sa.Integer(), nullable=False, server_default='1'))
    op.create_index(op.f('ix_categories_hospital_id'), 'categories', ['hospital_id'], unique=False)
    op.create_foreign_key(op.f('categories_hospital_id_fkey'), 'categories', 'hospitals', ['hospital_id'], ['id'], ondelete='CASCADE')
    op.alter_column('categories', 'hospital_id', server_default=None)

    # Add hospital_id column to subcategories table
    op.add_column('subcategories', sa.Column('hospital_id', sa.Integer(), nullable=False, server_default='1'))
    op.create_index(op.f('ix_subcategories_hospital_id'), 'subcategories', ['hospital_id'], unique=False)
    op.create_foreign_key(op.f('subcategories_hospital_id_fkey'), 'subcategories', 'hospitals', ['hospital_id'], ['id'], ondelete='CASCADE')
    op.alter_column('subcategories', 'hospital_id', server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    # Remove hospital_id from subcategories
    op.drop_constraint(op.f('subcategories_hospital_id_fkey'), 'subcategories', type_='foreignkey')
    op.drop_index(op.f('ix_subcategories_hospital_id'), table_name='subcategories')
    op.drop_column('subcategories', 'hospital_id')

    # Remove hospital_id from categories
    op.drop_constraint(op.f('categories_hospital_id_fkey'), 'categories', type_='foreignkey')
    op.drop_index(op.f('ix_categories_hospital_id'), table_name='categories')
    op.drop_column('categories', 'hospital_id')
