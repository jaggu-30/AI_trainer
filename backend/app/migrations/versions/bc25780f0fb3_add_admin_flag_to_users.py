"""add admin flag to users

Revision ID: bc25780f0fb3
Revises: 72a6c1482fd3
Create Date: 2026-09-13 12:11:41.199390

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision: str = "bc25780f0fb3"
down_revision: Union[str, None] = "72a6c1482fd3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, None] = None


def upgrade() -> None:
    """
    Add the administrator flag when it does not already exist.
    """

    bind = op.get_bind()
    inspector = sa.inspect(bind)

    columns = {
        column["name"]
        for column in inspector.get_columns("users")
    }

    if "is_admin" not in columns:
        op.add_column(
            "users",
            sa.Column(
                "is_admin",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            ),
        )


def downgrade() -> None:
    """
    Remove the administrator flag when it exists.
    """

    bind = op.get_bind()
    inspector = sa.inspect(bind)

    columns = {
        column["name"]
        for column in inspector.get_columns("users")
    }

    if "is_admin" in columns:
        op.drop_column(
            "users",
            "is_admin",
        )