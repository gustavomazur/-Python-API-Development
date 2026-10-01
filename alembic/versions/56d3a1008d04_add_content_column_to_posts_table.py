"""add content column to posts table

Revision ID: 56d3a1008d04
Revises: 6701cded4880
Create Date: 2026-09-30 12:16:56.406819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56d3a1008d04'
down_revision: Union[str, Sequence[str], None] = '6701cded4880'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'contenta')
    pass
