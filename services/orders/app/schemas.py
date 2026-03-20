import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models import OrderStatus


# ── OrderItem Schemas ─────────────────────────────────────────
class OrderItemCreate(BaseModel):
    product_name: str
    quantity: int = Field(ge=1, default=1)
    unit_price: Decimal = Field(ge=0)


class OrderItemResponse(BaseModel):
    id: uuid.UUID
    product_name: str
    quantity: int
    unit_price: Decimal

    model_config = {"from_attributes": True}


# ── Order Schemas ─────────────────────────────────────────────
class OrderCreate(BaseModel):
    customer_name: str
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderResponse(BaseModel):
    id: uuid.UUID
    customer_name: str
    status: OrderStatus
    total: Decimal
    user_id: str
    items: list[OrderItemResponse]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
