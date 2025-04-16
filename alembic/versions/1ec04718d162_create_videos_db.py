"""Create Videos DB

Revision ID: 1ec04718d162
Revises: 9ab391020287
Create Date: 2025-04-08 19:34:20.840570

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1ec04718d162"
down_revision: Union[str, None] = "9ab391020287"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "videos",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("title", sa.VARCHAR(), nullable=False),
        sa.Column("file_path", sa.VARCHAR(), nullable=False),
        sa.Column("zip_path", sa.VARCHAR(), nullable=True),
        sa.Column(
            "status",
            sa.VARCHAR(),
            server_default=sa.text("'processing'"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.INTEGER(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("videos")
