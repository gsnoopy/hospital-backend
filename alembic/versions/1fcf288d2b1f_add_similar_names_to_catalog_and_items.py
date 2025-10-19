"""add_similar_names_to_catalog_and_items

Revision ID: 1fcf288d2b1f
Revises: 2427c46474a7
Create Date: 2025-10-19 05:47:59.279047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '1fcf288d2b1f'
down_revision: Union[str, Sequence[str], None] = '2427c46474a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add similar_names column to catalog table
    op.add_column('catalog', sa.Column('similar_names', postgresql.ARRAY(sa.String()), nullable=True))

    # Add similar_names column to items table
    op.add_column('items', sa.Column('similar_names', postgresql.ARRAY(sa.String()), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove similar_names column from items table
    op.drop_column('items', 'similar_names')

    # Remove similar_names column from catalog table
    op.drop_column('catalog', 'similar_names')
