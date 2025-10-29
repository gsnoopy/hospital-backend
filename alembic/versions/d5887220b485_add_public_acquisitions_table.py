"""Add public_acquisitions table

Revision ID: d5887220b485
Revises: 20fac09fedcd
Create Date: 2025-10-28 23:27:28.853169

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd5887220b485'
down_revision: Union[str, Sequence[str], None] = '20fac09fedcd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create public_acquisitions table
    op.create_table('public_acquisitions',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('public_id', postgresql.UUID(), nullable=False),
        sa.Column('code', sa.VARCHAR(), nullable=False),
        sa.Column('title', sa.VARCHAR(), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(), nullable=True),
        sa.Column('hospital_id', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['hospital_id'], ['hospitals.id'], name='public_acquisitions_hospital_id_fkey', ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id', name='public_acquisitions_pkey')
    )
    op.create_index('ix_public_acquisitions_id', 'public_acquisitions', ['id'], unique=False)
    op.create_index('ix_public_acquisitions_public_id', 'public_acquisitions', ['public_id'], unique=True)
    op.create_index('ix_public_acquisitions_code', 'public_acquisitions', ['code'], unique=False)
    op.create_index('ix_public_acquisitions_title', 'public_acquisitions', ['title'], unique=False)
    op.create_index('ix_public_acquisitions_hospital_id', 'public_acquisitions', ['hospital_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_public_acquisitions_hospital_id', table_name='public_acquisitions')
    op.drop_index('ix_public_acquisitions_title', table_name='public_acquisitions')
    op.drop_index('ix_public_acquisitions_code', table_name='public_acquisitions')
    op.drop_index('ix_public_acquisitions_public_id', table_name='public_acquisitions')
    op.drop_index('ix_public_acquisitions_id', table_name='public_acquisitions')
    op.drop_table('public_acquisitions')
