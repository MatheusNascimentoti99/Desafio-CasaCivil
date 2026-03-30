import uuid
from datetime import datetime
from decimal import Decimal
import enum

from pydantic import BaseModel, Field, PositiveFloat


class OrderStatus(str, enum.Enum):
    PENDING = "pendente"
    CONFIRMED = "confirmado"
    SHIPPED = "enviado"
    DELIVERED = "entregue"
    CANCELLED = "cancelado"


class OrderItemCreate(BaseModel):
    product_ean: str = Field(min_length=8, max_length=14, pattern=r"^\d{8,14}$")
    quantity: int = Field(ge=1, default=1)


class OrderItemResponse(BaseModel):
    id: uuid.UUID
    product_ean: str = Field(min_length=8, max_length=14, pattern=r"^\d{8,14}$")
    quantity: int
    unit_price: PositiveFloat

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=255)
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderResponse(BaseModel):
    id: uuid.UUID
    customer_name: str = Field(min_length=2, max_length=255)
    status: OrderStatus
    total: Decimal
    user_id: str
    items: list[OrderItemResponse]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
