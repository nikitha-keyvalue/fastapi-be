import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers import orders as ctrl
from app.deps import CurrentUserDep, get_db
from app.schemas.order import OrderCreate, OrderDetailOut, OrderOut, OrderUpdate

router = APIRouter()


@router.post("", response_model=OrderDetailOut, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    current_user: CurrentUserDep,
    db: Session = Depends(get_db),
):
    return ctrl.create_order(payload, current_user, db)


@router.get("", response_model=list[OrderOut])
def list_my_orders(
    current_user: CurrentUserDep,
    db: Session = Depends(get_db),
):
    return ctrl.list_my_orders(current_user, db)


@router.get("/{order_id}", response_model=OrderDetailOut)
def get_order(
    order_id: uuid.UUID,
    current_user: CurrentUserDep,
    db: Session = Depends(get_db),
):
    return ctrl.get_order(order_id, current_user, db)


@router.patch("/{order_id}", response_model=OrderDetailOut)
def update_order(
    order_id: uuid.UUID,
    payload: OrderUpdate,
    current_user: CurrentUserDep,
    db: Session = Depends(get_db),
):
    return ctrl.update_order(order_id, payload, current_user, db)


@router.post("/{order_id}/cancel", response_model=OrderDetailOut)
def cancel_order(
    order_id: uuid.UUID,
    current_user: CurrentUserDep,
    db: Session = Depends(get_db),
):
    return ctrl.cancel_order(order_id, current_user, db)
