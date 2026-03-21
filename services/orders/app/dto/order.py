import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.dao import OrderStatus
from app.dto.order_item import OrderItemCreate, OrderItemResponse


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
