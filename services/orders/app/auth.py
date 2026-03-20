"""
JWT token validation for the Orders service (RS256).
Uses the PUBLIC key to verify tokens signed by the Auth service.
This service does NOT have access to the private key — it cannot forge tokens.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from app.config import settings

security = HTTPBearer()


class TokenData(BaseModel):
    sub: str  # email of the authenticated user


def get_current_user_email(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Decode and validate the JWT token using the PUBLIC key,
    returning the user email (sub claim).
    """
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.public_key,
            algorithms=[settings.JWT_ALGORITHM],
        )
        sub: str | None = payload.get("sub")
        if sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )
        return sub
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )
