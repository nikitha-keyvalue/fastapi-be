from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product


def list_active_products(db: Session) -> list[Product]:
    stmt = (
        select(Product).where(Product.is_active.is_(True)).order_by(Product.name)
    )
    return list(db.scalars(stmt))
