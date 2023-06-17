"""create user table

Revision ID: 4f80c20e99a3
Revises:
Create Date: 2023-06-17 16:07:00.062420

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "4f80c20e99a3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
    )


def downgrade() -> None:
    pass
