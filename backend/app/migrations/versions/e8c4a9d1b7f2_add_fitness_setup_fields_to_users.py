"""add saved fitness setup fields to users

Revision ID: e8c4a9d1b7f2
Revises: bc25780f0fb3
Create Date: 2026-09-20
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e8c4a9d1b7f2"
down_revision: Union[str, None] = "bc25780f0fb3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    columns = {
        column["name"]
        for column in sa.inspect(bind).get_columns("users")
    }

    if "sex" not in columns:
        op.add_column("users", sa.Column("sex", sa.String(length=20), nullable=True))

    if "workout_preference" not in columns:
        op.add_column(
            "users",
            sa.Column("workout_preference", sa.String(length=50), nullable=True),
        )


def downgrade() -> None:
    bind = op.get_bind()
    columns = {
        column["name"]
        for column in sa.inspect(bind).get_columns("users")
    }

    if "workout_preference" in columns:
        op.drop_column("users", "workout_preference")

    if "sex" in columns:
        op.drop_column("users", "sex")
