import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.order import OrderStatus


# ── Create ───────────────────────────────────────────────────────────────

class OrderItemCreate(BaseModel):
    product_id: uuid.UUID
    quantity: int = Field(gt=0, description="Must be at least 1")


class OrderCreate(BaseModel):
    items: list[OrderItemCreate] = Field(min_length=1, description="At least one item required")


# ── Update (only pending orders) ─────────────────────────────────────────

class OrderItemUpdate(BaseModel):
    product_id: uuid.UUID
    quantity: int = Field(gt=0)


class OrderUpdate(BaseModel):
    items: list[OrderItemUpdate] = Field(min_length=1, description="Full replacement of order items")


# ── Response ─────────────────────────────────────────────────────────────

class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    unit_price: Decimal
    total_price: Decimal


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    status: OrderStatus
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime


class OrderDetailOut(OrderOut):
    items: list[OrderItemOut] = []
