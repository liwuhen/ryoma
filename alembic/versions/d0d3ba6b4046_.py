"""empty message

Revision ID: d0d3ba6b4046
Revises: 
Create Date: 2024-07-24 09:13:25.640554

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d0d3ba6b4046"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "catalogtable",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("datasource_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("catalog_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("schema", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("table", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "chat",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("user", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("question", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("answer", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("created_at", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("updated_at", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "datasource",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("datasource", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("connection_url", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created_at", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("updated_at", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "vectorstore",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("online_store_type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("offline_store_type", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("online_store_configs", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("offline_store_configs", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("vectorstore")
    op.drop_table("user")
    op.drop_table("datasource")
    op.drop_table("chat")
    op.drop_table("catalogtable")
    # ### end Alembic commands ###
