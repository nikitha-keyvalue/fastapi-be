import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.exceptions import BadRequestError, ConflictError, ForbiddenError, NotFoundError
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.product import Product


# ── internal helpers ─────────────────────────────────────────────────────

def _enforce_ownership(order: Order, user_id: uuid.UUID) -> None:
    if order.user_id != user_id:
        raise ForbiddenError("Not your order")


def _enforce_pending(order: Order) -> None:
    if order.status != OrderStatus.pending:
        raise ConflictError(f"Cannot modify order with status '{order.status.value}'")


def _validate_and_fetch_products(
    product_ids: list[uuid.UUID],
    db: Session,
) -> dict[uuid.UUID, Product]:
    if len(product_ids) != len(set(product_ids)):
        raise BadRequestError("Duplicate product IDs in items")

    products = list(
        db.scalars(select(Product).where(Product.id.in_(product_ids)))
    )
    product_map = {p.id: p for p in products}

    missing = [str(pid) for pid in product_ids if pid not in product_map]
    if missing:
        raise NotFoundError(f"Products not found: {', '.join(missing)}")

    inactive = [str(pid) for pid in product_ids if not product_map[pid].is_active]
    if inactive:
        raise BadRequestError(f"Inactive products: {', '.join(inactive)}")

    return product_map


def _check_stock(
    product_map: dict[uuid.UUID, Product],
    items: list[tuple[uuid.UUID, int]],
) -> None:
    insufficient: list[str] = []
    for pid, qty in items:
        p = product_map[pid]
        if p.stock_quantity < qty:
            insufficient.append(
                f"{p.name} (requested {qty}, available {p.stock_quantity})"
            )
    if insufficient:
        raise ConflictError(f"Insufficient stock: {'; '.join(insufficient)}")


def _get_order_with_items(db: Session, order_id: uuid.UUID) -> Order:
    order = db.scalars(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order_id)
    ).first()
    if order is None:
        raise NotFoundError("Order not found")
    return order


def _build_items(
    order: Order,
    pid_qty: list[tuple[uuid.UUID, int]],
    product_map: dict[uuid.UUID, Product],
) -> Decimal:
    """Append OrderItems to *order*, deduct stock, return total amount."""
    total = Decimal("0.00")
    for pid, qty in pid_qty:
        product = product_map[pid]
        unit_price = product.price
        line_total = unit_price * qty
        total += line_total

        order.items.append(
            OrderItem(
                product_id=pid,
                quantity=qty,
                unit_price=unit_price,
                total_price=line_total,
            )
        )
        product.stock_quantity -= qty
    return total


def _restore_stock(db: Session, items: list[OrderItem]) -> None:
    for oi in items:
        product = db.get(Product, oi.product_id)
        if product is not None:
            product.stock_quantity += oi.quantity


# ── public service API ───────────────────────────────────────────────────

def create_order(
    db: Session,
    *,
    user_id: uuid.UUID,
    items: list[tuple[uuid.UUID, int]],
) -> Order:
    product_ids = [pid for pid, _ in items]
    product_map = _validate_and_fetch_products(product_ids, db)
    _check_stock(product_map, items)

    order = Order(user_id=user_id, status=OrderStatus.pending)
    order.total_amount = _build_items(order, items, product_map)

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def list_user_orders(db: Session, *, user_id: uuid.UUID) -> list[Order]:
    stmt = (
        select(Order)
        .where(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
    )
    return list(db.scalars(stmt))


def get_user_order(
    db: Session,
    *,
    order_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Order:
    order = _get_order_with_items(db, order_id)
    _enforce_ownership(order, user_id)
    return order


def update_order(
    db: Session,
    *,
    order_id: uuid.UUID,
    user_id: uuid.UUID,
    items: list[tuple[uuid.UUID, int]],
) -> Order:
    order = _get_order_with_items(db, order_id)
    _enforce_ownership(order, user_id)
    _enforce_pending(order)

    product_ids = [pid for pid, _ in items]
    product_map = _validate_and_fetch_products(product_ids, db)

    _restore_stock(db, order.items)
    _check_stock(product_map, items)

    for oi in list(order.items):
        db.delete(oi)
    order.items.clear()

    order.total_amount = _build_items(order, items, product_map)

    db.commit()
    db.refresh(order)
    return order


def cancel_order(
    db: Session,
    *,
    order_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Order:
    order = _get_order_with_items(db, order_id)
    _enforce_ownership(order, user_id)
    _enforce_pending(order)

    _restore_stock(db, order.items)
    order.status = OrderStatus.cancelled

    db.commit()
    db.refresh(order)
    return order
