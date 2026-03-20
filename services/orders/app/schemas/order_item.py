import uuid
from decimal import Decimal

from pydantic import BaseModel, Field


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
