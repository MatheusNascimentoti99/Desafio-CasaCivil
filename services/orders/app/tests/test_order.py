import pytest
from decimal import Decimal
from sqlalchemy import delete
from app.models import Order, OrderItem
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import OrderCreate, OrderItemCreate, OrderStatus
from app.services.order import (
    create_order,
    get_allowed_status_transitions,
    get_order_by_id,
    get_orders,
    update_order_status,
)

async def clear_orders_table(session: AsyncSession) -> None:
    """Clear all orders and items from the tables."""
    stmt_items = delete(OrderItem)
    stmt_orders = delete(Order)
    await session.execute(stmt_items)
    await session.execute(stmt_orders)
    await session.commit()


@pytest.fixture(autouse=True)
async def cleanup_orders(db: AsyncSession):
    """Automatically clear orders and items tables after each test."""
    yield
    await clear_orders_table(db)

@pytest.fixture
def order_data():
    """Fixture que retorna dados para criar um pedido."""
    return OrderCreate(
        customer_name="João Silva",
        items=[
            OrderItemCreate(
                product_name="Notebook",
                quantity=1,
                unit_price=Decimal("1500.00"),
            ),
            OrderItemCreate(
                product_name="Mouse",
                quantity=2,
                unit_price=Decimal("50.00"),
            ),
        ],
    )


@pytest.fixture
def user_email():
    """Fixture que retorna um email de usuário para teste."""
    return "joao@example.com"


@pytest.mark.asyncio
async def test_create_order(db: AsyncSession, order_data, user_email):
    """Testa criação de um pedido."""
    order = await create_order(db, order_data, user_email)

    assert order.id is not None
    assert order.customer_name == order_data.customer_name
    assert order.user_id == user_email
    assert order.status == OrderStatus.PENDING
    assert len(order.items) == 2
    # Total esperado: 1500 + (50 * 2) = 1600
    assert order.total == Decimal("1600.00")


@pytest.mark.asyncio
async def test_get_order_by_id(db: AsyncSession, order_data, user_email):
    """Testa busca de pedido por ID."""
    # Criar um pedido
    created_order = await create_order(db, order_data, user_email)

    # Buscar pelo ID
    fetched_order = await get_order_by_id(db, created_order.id)

    assert fetched_order is not None
    assert fetched_order.id == created_order.id
    assert fetched_order.customer_name == order_data.customer_name
    assert fetched_order.user_id == user_email


@pytest.mark.asyncio
async def test_get_orders_list(db: AsyncSession, order_data, user_email):
    """Testa listagem de pedidos."""
    # Criar múltiplos pedidos
    order1 = await create_order(db, order_data, user_email)
    
    order_data2 = OrderCreate(
        customer_name="Maria Santos",
        items=[
            OrderItemCreate(
                product_name="Teclado",
                quantity=1,
                unit_price=Decimal("200.00"),
            ),
        ],
    )
    order2 = await create_order(db, order_data2, "maria@example.com")

    # Listar todos os pedidos
    orders = await get_orders(db, skip=0, limit=10)

    assert isinstance(orders, list)
    assert len(orders) == 2
    assert any(o.id == order1.id for o in orders)
    assert any(o.id == order2.id for o in orders)


@pytest.mark.asyncio
async def test_get_orders_with_status_filter(db: AsyncSession, order_data, user_email):
    """Testa listagem de pedidos com filtro de status."""
    # Criar um pedido e mudar seu status
    order = await create_order(db, order_data, user_email)
    await update_order_status(db, order.id, OrderStatus.CONFIRMED)

    # Listar apenas pedidos CONFIRMED
    confirmed_orders = await get_orders(db, status_filter=OrderStatus.CONFIRMED)
    
    # Listar apenas pedidos PENDING
    pending_orders = await get_orders(db, status_filter=OrderStatus.PENDING)

    assert len(confirmed_orders) >= 1
    assert any(o.id == order.id for o in confirmed_orders)
    assert len(pending_orders) == 0


@pytest.mark.asyncio
async def test_update_order_status(db: AsyncSession, order_data, user_email):
    """Testa atualização de status do pedido."""
    # Criar um pedido
    order = await create_order(db, order_data, user_email)
    assert order.status == OrderStatus.PENDING

    # Atualizar para CONFIRMED
    updated_order = await update_order_status(db, order.id, OrderStatus.CONFIRMED)
    assert updated_order is not None
    assert updated_order.status == OrderStatus.CONFIRMED

    # Atualizar para SHIPPED
    updated_order = await update_order_status(db, order.id, OrderStatus.SHIPPED)
    assert updated_order is not None
    assert updated_order.status == OrderStatus.SHIPPED

    # Atualizar para DELIVERED
    updated_order = await update_order_status(db, order.id, OrderStatus.DELIVERED)
    assert updated_order is not None
    assert updated_order.status == OrderStatus.DELIVERED


@pytest.mark.asyncio
async def test_status_transitions_rules(db: AsyncSession, order_data, user_email):
    order = await create_order(db, order_data, user_email)

    assert get_allowed_status_transitions(OrderStatus.PENDING) == {
        OrderStatus.CONFIRMED,
        OrderStatus.CANCELLED,
    }

    await update_order_status(db, order.id, OrderStatus.CONFIRMED)
    updated_order = await get_order_by_id(db, order.id)
    assert updated_order is not None
    assert get_allowed_status_transitions(updated_order.status) == {
        OrderStatus.SHIPPED,
        OrderStatus.CANCELLED,
    }


@pytest.mark.asyncio
async def test_delivered_cannot_be_cancelled(db: AsyncSession, order_data, user_email):
    order = await create_order(db, order_data, user_email)
    await update_order_status(db, order.id, OrderStatus.CONFIRMED)
    await update_order_status(db, order.id, OrderStatus.SHIPPED)
    await update_order_status(db, order.id, OrderStatus.DELIVERED)

    with pytest.raises(ValueError):
        await update_order_status(db, order.id, OrderStatus.CANCELLED)


@pytest.mark.asyncio
async def test_cancelled_cannot_change_status(db: AsyncSession, order_data, user_email):
    order = await create_order(db, order_data, user_email)
    await update_order_status(db, order.id, OrderStatus.CANCELLED)

    with pytest.raises(ValueError):
        await update_order_status(db, order.id, OrderStatus.CONFIRMED)


@pytest.mark.asyncio
async def test_order_items_cascade(db: AsyncSession, order_data, user_email):
    """Testa que items são deletados quando a ordem é deletada (cascade)."""
    # Criar um pedido
    order = await create_order(db, order_data, user_email)
    order_id = order.id
    assert len(order.items) == 2

    # Verificar que os items foram criados
    fetched_order = await get_order_by_id(db, order_id)
    assert len(fetched_order.items) == 2


@pytest.mark.asyncio
async def test_order_total_calculation(db: AsyncSession, user_email):
    """Testa cálculo correto do total do pedido."""
    order_data = OrderCreate(
        customer_name="Test Customer",
        items=[
            OrderItemCreate(
                product_name="Item A",
                quantity=2,
                unit_price=Decimal("100.00"),
            ),
            OrderItemCreate(
                product_name="Item B",
                quantity=3,
                unit_price=Decimal("50.00"),
            ),
            OrderItemCreate(
                product_name="Item C",
                quantity=1,
                unit_price=Decimal("25.50"),
            ),
        ],
    )
    
    order = await create_order(db, order_data, user_email)
    
    # Total esperado: (2*100) + (3*50) + (1*25.50) = 200 + 150 + 25.50 = 375.50
    assert order.total == Decimal("375.50")
    assert len(order.items) == 3
