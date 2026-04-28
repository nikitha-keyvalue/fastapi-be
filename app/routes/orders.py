from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.deps import CurrentUserDep, get_db
from app.models.order import Order
from app.schemas.order import OrderOut

router = APIRouter()


@router.get("", response_model=list[OrderOut])
def list_my_orders(
    current_user: CurrentUserDep,
    db: Session = Depends(get_db),
) -> list[Order]:
    stmt = (
        select(Order)
        .where(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
    )
    return list(db.scalars(stmt))
