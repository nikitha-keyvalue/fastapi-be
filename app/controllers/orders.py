import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.exceptions import BadRequestError, ConflictError, ForbiddenError, NotFoundError
from app.models.order import Order
from app.models.user import User
from app.schemas.order import OrderCreate, OrderUpdate
from app.services import order_service


def _map_service_exceptions(exc: Exception) -> HTTPException:
    if isinstance(exc, NotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.detail)
    if isinstance(exc, ForbiddenError):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.detail)
    if isinstance(exc, ConflictError):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail)
    if isinstance(exc, BadRequestError):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.detail)
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error")


def create_order(payload: OrderCreate, current_user: User, db: Session) -> Order:
    items = [(item.product_id, item.quantity) for item in payload.items]
    try:
        return order_service.create_order(db, user_id=current_user.id, items=items)
    except (NotFoundError, BadRequestError, ConflictError) as exc:
        raise _map_service_exceptions(exc) from exc


def list_my_orders(current_user: User, db: Session) -> list[Order]:
    return order_service.list_user_orders(db, user_id=current_user.id)


def get_order(order_id: uuid.UUID, current_user: User, db: Session) -> Order:
    try:
        return order_service.get_user_order(db, order_id=order_id, user_id=current_user.id)
    except (NotFoundError, ForbiddenError) as exc:
        raise _map_service_exceptions(exc) from exc


def update_order(
    order_id: uuid.UUID, payload: OrderUpdate, current_user: User, db: Session,
) -> Order:
    items = [(item.product_id, item.quantity) for item in payload.items]
    try:
        return order_service.update_order(
            db, order_id=order_id, user_id=current_user.id, items=items,
        )
    except (NotFoundError, ForbiddenError, ConflictError, BadRequestError) as exc:
        raise _map_service_exceptions(exc) from exc


def cancel_order(order_id: uuid.UUID, current_user: User, db: Session) -> Order:
    try:
        return order_service.cancel_order(db, order_id=order_id, user_id=current_user.id)
    except (NotFoundError, ForbiddenError, ConflictError) as exc:
        raise _map_service_exceptions(exc) from exc
