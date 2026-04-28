from sqlalchemy.orm import Session

from app.models.product import Product
from app.services import product_service


def list_products(db: Session) -> list[Product]:
    return product_service.list_active_products(db)
