import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user_email
from app.services import create_order, get_order_by_id, get_orders, update_order_status
from app.database import get_db
from app.models import OrderStatus
from app.schemas import OrderCreate, OrderResponse, OrderStatusUpdate

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get(
    "/",
    response_model=list[OrderResponse],
    summary="Listar pedidos com filtro opcional por status",
)
async def list_orders(
    status_filter: OrderStatus | None = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _user_email: str = Depends(get_current_user_email),
):
    orders = await get_orders(db, status_filter=status_filter, skip=skip, limit=limit)
    return orders


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo pedido",
)
async def create_new_order(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_db),
    user_email: str = Depends(get_current_user_email),
):
    order = await create_order(db, order_in, user_email)
    return order


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Consultar pedido por ID",
)
async def get_order(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user_email: str = Depends(get_current_user_email),
):
    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado",
        )
    return order


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
    summary="Atualizar status do pedido",
)
async def patch_order_status(
    order_id: uuid.UUID,
    body: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    _user_email: str = Depends(get_current_user_email),
):
    order = await update_order_status(db, order_id, body.status)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado",
        )
    return order
