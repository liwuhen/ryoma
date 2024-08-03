"""empty message

Revision ID: 9f42e76c9deb
Revises: 
Create Date: 2024-08-01 17:06:25.125437

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9f42e76c9deb"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "catalog",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("datasource", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("database", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "playground",
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
        sa.Column("connection_url", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("attributes", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("catalog_id", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "prompttemplate",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("prompt_repr", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("k_shot", sa.Integer(), nullable=False),
        sa.Column("example_format", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("selector_type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("prompt_template_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("prompt_lines", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("prompt_template_type", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
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
        sa.Column("online_store", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("offline_store", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("online_store_configs", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("offline_store_configs", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "schema",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("catalog_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["catalog_id"],
            ["catalog.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("is_view", sa.Boolean(), nullable=True),
        sa.Column("attrs", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("schema_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["schema_id"],
            ["schema.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "column",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("table_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["table_id"],
            ["table.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("column")
    op.drop_table("table")
    op.drop_table("schema")
    op.drop_table("vectorstore")
    op.drop_table("user")
    op.drop_table("prompttemplate")
    op.drop_table("datasource")
    op.drop_table("playground")
    op.drop_table("catalog")
    # ### end Alembic commands ###
