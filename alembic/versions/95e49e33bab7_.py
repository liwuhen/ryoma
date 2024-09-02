"""empty message

Revision ID: 95e49e33bab7
Revises: 079536e22d00
Create Date: 2024-09-02 12:06:05.158939

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "95e49e33bab7"
down_revision: Union[str, None] = "079536e22d00"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("vectorstore", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "project_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False
            )
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("vectorstore", schema=None) as batch_op:
        batch_op.drop_column("project_name")

    # ### end Alembic commands ###