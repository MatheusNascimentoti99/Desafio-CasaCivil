from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import (
    create_access_token,
    get_current_user,
    verify_password,
)
from app.crud import create_user, get_user_by_email, get_users
from app.database import get_db
from app.models import User
from app.schemas import Token, UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar novo usuário",
)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado",
        )
    user = await create_user(db, user_in)
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Autenticar e receber token JWT",
)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, credentials.email)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )
    token = create_access_token(data={"sub": user.email})
    return Token(access_token=token)


@router.get(
    "/users",
    response_model=list[UserResponse],
    summary="Listar todos os usuários",
)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    users = await get_users(db, skip=skip, limit=limit)
    return users


@router.get(
    "/users/me",
    response_model=UserResponse,
    summary="Dados do usuário autenticado",
)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
