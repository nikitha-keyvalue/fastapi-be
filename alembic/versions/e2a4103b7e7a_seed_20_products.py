"""seed 20 products

Revision ID: e2a4103b7e7a
Revises: 74f200d2aa13
Create Date: 2026-03-04 13:46:30.409624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime
import uuid


# revision identifiers, used by Alembic.
revision: str = 'e2a4103b7e7a'
down_revision: Union[str, Sequence[str], None] = '74f200d2aa13'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    products_table = sa.table(
        "products",
        sa.column("id", postgresql.UUID(as_uuid=True)),
        sa.column("name", sa.String(length=255)),
        sa.column("description", sa.Text),
        sa.column("price", sa.Numeric(10, 2)),
        sa.column("stock_quantity", sa.Integer),
        sa.column("is_active", sa.Boolean),
        sa.column("created_at", sa.DateTime),
        sa.column("updated_at", sa.DateTime),
    )

    now = datetime.utcnow()

    op.bulk_insert(
        products_table,
        [
            {
                "id": uuid.uuid4(),
                "name": f"Product {i}",
                "description": f"High quality product number {i}",
                "price": round(50 + i * 7.5, 2),
                "stock_quantity": 100 + i,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            }
            for i in range(1, 21)
        ],
    )


def downgrade():
    op.execute("DELETE FROM products;")
