"""add content column to ther post table

Revision ID: 5cb70b0a38d7
Revises: 9a84b692c137
Create Date: 2023-09-22 16:44:16.113307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5cb70b0a38d7'
down_revision: Union[str, None] = '9a84b692c137'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
