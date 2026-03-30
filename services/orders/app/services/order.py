import uuid
from decimal import Decimal

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models import Order, OrderItem, OrderStatus
from app.schemas import OrderCreate


STATUS_NEXT_TRANSITION: dict[OrderStatus, OrderStatus] = {
    OrderStatus.PENDING: OrderStatus.CONFIRMED,
    OrderStatus.CONFIRMED: OrderStatus.SHIPPED,
    OrderStatus.SHIPPED: OrderStatus.DELIVERED,
}


def get_allowed_status_transitions(current_status: OrderStatus) -> set[OrderStatus]:
    if current_status == OrderStatus.CANCELLED:
        return set()

    allowed: set[OrderStatus] = set()
    next_status = STATUS_NEXT_TRANSITION.get(current_status)
    if next_status:
        allowed.add(next_status)

    if current_status != OrderStatus.DELIVERED:
        allowed.add(OrderStatus.CANCELLED)

    return allowed


async def get_orders(
    db: AsyncSession,
    status_filter: OrderStatus | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[Order]:
    query = select(Order).offset(skip).limit(limit).order_by(Order.created_at.desc())
    if status_filter:
        query = query.where(Order.status == status_filter)
    result = await db.execute(query)
    return list(result.scalars().unique().all())


async def get_order_by_id(db: AsyncSession, order_id: uuid.UUID) -> Order | None:
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()


async def create_order(
    db: AsyncSession, order_in: OrderCreate, user_email: str
) -> Order:
    product_prices = await fetch_products_prices_by_ean(
        {item.product_ean for item in order_in.items}
    )

    # Calculate total from items
    total = Decimal("0")
    items = []
    for item_data in order_in.items:
        unit_price = product_prices[item_data.product_ean]
        total += unit_price * item_data.quantity
        items.append(
            OrderItem(
                product_ean=item_data.product_ean,
                quantity=item_data.quantity,
                unit_price=unit_price,
            )
        )

    order = Order(
        customer_name=order_in.customer_name,
        total=total,
        user_id=user_email,
        items=items,
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def fetch_products_prices_by_ean(product_eans: set[str]) -> dict[str, Decimal]:
    prices: dict[str, Decimal] = {}

    async with httpx.AsyncClient(timeout=10.0) as client:
        for ean in product_eans:
            response = await client.get(
                f"{settings.CATALOG_SERVICE_URL}/api/catalog/products/{ean}"
            )

            if response.status_code == 404:
                raise ValueError(f"Produto com EAN {ean} não encontrado no catálogo")

            if response.status_code >= 400:
                raise ValueError("Falha ao consultar catálogo de produtos")

            payload = response.json()
            prices[ean] = Decimal(str(payload["unit_price"]))

    return prices


async def update_order_status(
    db: AsyncSession, order_id: uuid.UUID, new_status: OrderStatus
) -> Order | None:
    order = await get_order_by_id(db, order_id)
    if not order:
        return None

    if order.status == new_status:
        return order

    allowed_statuses = get_allowed_status_transitions(order.status)
    if new_status not in allowed_statuses:
        allowed_values = ", ".join(sorted(status.value for status in allowed_statuses))
        raise ValueError(
            "Transição de status inválida: "
            f"{order.status.value} -> {new_status.value}. "
            f"Próximos status permitidos: [{allowed_values}]"
        )

    order.status = new_status
    await db.commit()
    await db.refresh(order)
    return order
