from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    ean: str = Field(min_length=8, max_length=14, pattern=r"^\\d{8,14}$")
    name: str = Field(min_length=2, max_length=255)
    unit_price: Decimal = Field(gt=0)


class ProductResponse(BaseModel):
    ean: str = Field(min_length=8, max_length=14, pattern=r"^\\d{8,14}$")
    name: str
    unit_price: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
