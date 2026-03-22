import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, StrictStr, StrictBool, Field


class UserCreate(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=255)
    full_name: str = Field(min_length=2, max_length=255)


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)
    is_active: StrictBool = True
    created_at: datetime

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=255)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: str | None = None
