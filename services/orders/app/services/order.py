import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import Order, OrderItem, OrderStatus
from app.dto import OrderCreate


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
    # Calculate total from items
    total = Decimal("0")
    items = []
    for item_data in order_in.items:
        total += item_data.unit_price * item_data.quantity
        items.append(
            OrderItem(
                product_name=item_data.product_name,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
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


async def update_order_status(
    db: AsyncSession, order_id: uuid.UUID, new_status: OrderStatus
) -> Order | None:
    order = await get_order_by_id(db, order_id)
    if not order:
        return None
    order.status = new_status
    await db.commit()
    await db.refresh(order)
    return order
