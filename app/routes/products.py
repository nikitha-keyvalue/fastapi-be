from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import products as ctrl
from app.deps import get_db
from app.schemas.product import ProductOut

router = APIRouter()


@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return ctrl.list_products(db)
