from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models.product import Product
from app.schemas.product import ProductOut

router = APIRouter()


@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)) -> list[Product]:
    stmt = (
        select(Product).where(Product.is_active.is_(True)).order_by(Product.name)
    )
    return list(db.scalars(stmt))
