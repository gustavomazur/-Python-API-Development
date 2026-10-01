"""add foreign-key to posts table

Revision ID: 64ca392b9620
Revises: c44764ca1b29
Create Date: 2026-09-30 13:56:03.642444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64ca392b9620'
down_revision: Union[str, Sequence[str], None] = 'c44764ca1b29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk',source_table="posts",referent_table="users",
    local_cols=['user_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts','user_id')
    pass
