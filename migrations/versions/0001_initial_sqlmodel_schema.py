from __future__ import annotations

from alembic import op
from sqlmodel import SQLModel

import opennamu_forge.infrastructure.db_model  # noqa: F401

revision = "0001_initial_sqlmodel_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    SQLModel.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    SQLModel.metadata.drop_all(bind=op.get_bind())
