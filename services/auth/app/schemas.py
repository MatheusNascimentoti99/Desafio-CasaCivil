import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, StrictStr, StrictBool


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: StrictStr


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: StrictStr
    is_active: StrictBool = True
    created_at: datetime

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: str | None = None
