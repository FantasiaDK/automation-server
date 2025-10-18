"""add asset name and data fields

Revision ID: d4d1a2b3c4e5
Revises: a967e43074d6
Create Date: 2025-10-18 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd4d1a2b3c4e5'
down_revision: Union[str, None] = 'a967e43074d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    context = op.get_context()
    dialect_name = context.dialect.name

    # Use JSONB for Postgres, otherwise fallback to Text
    if dialect_name == "postgresql":
        target_json_type = postgresql.JSONB(astext_type=sa.Text())
    else:
        target_json_type = sa.Text()

    op.create_table(
        "asset",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column('data', target_json_type, nullable=False, server_default='{}'),
        sa.Column("deleted", sa.Boolean(), nullable=False, default=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    
    # Create unique index on name
    op.create_index(op.f('ix_asset_name'), 'asset', ['name'], unique=True)


def downgrade() -> None:
    # In downgrade, re-create the password column (nullable) and drop name and data
    # Re-add password column
    op.drop_index(op.f("ix_asset_name"), table_name="asset")
    op.drop_table("asset")
