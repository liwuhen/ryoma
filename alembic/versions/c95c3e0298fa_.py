"""empty message

Revision ID: c95c3e0298fa
Revises: e46bf1f7e482
Create Date: 2024-07-26 10:19:26.773327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'c95c3e0298fa'
down_revision: Union[str, None] = 'e46bf1f7e482'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('datasource', schema=None) as batch_op:
        batch_op.add_column(sa.Column('catalog_id', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('datasource', schema=None) as batch_op:
        batch_op.drop_column('catalog_id')

    # ### end Alembic commands ###
