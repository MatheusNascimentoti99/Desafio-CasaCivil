import pytest
from decimal import Decimal
from datetime import datetime
import uuid

from pydantic import ValidationError

from app.schemas import (
    OrderStatus,
    OrderItemCreate,
    OrderItemResponse,
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate,
)


class TestOrderStatus:
    """Testes para o enum OrderStatus."""

    def test_order_status_values(self):
        """Testa que todos os valores de status existem."""
        assert OrderStatus.PENDING.value == "pendente"
        assert OrderStatus.CONFIRMED.value == "confirmado"
        assert OrderStatus.SHIPPED.value == "enviado"
        assert OrderStatus.DELIVERED.value == "entregue"
        assert OrderStatus.CANCELLED.value == "cancelado"

    def test_order_status_count(self):
        """Testa que existem exatamente 5 status."""
        assert len(OrderStatus) == 5


class TestOrderItemCreate:
    """Testes para o schema OrderItemCreate."""

    def test_valid_order_item_create(self):
        """Testa criação válida de um item de pedido."""
        item = OrderItemCreate(
            product_name="Notebook",
            quantity=1,
            unit_price=Decimal("1500.00"),
        )
        assert item.product_name == "Notebook"
        assert item.quantity == 1
        assert item.unit_price == Decimal("1500.00")

    def test_order_item_create_with_defaults(self):
        """Testa que quantidade padrão é 1."""
        item = OrderItemCreate(
            product_name="Mouse",
            unit_price=Decimal("50.00"),
        )
        assert item.quantity == 1

    def test_order_item_create_invalid_quantity_zero(self):
        """Testa que quantidade não pode ser zero."""
        with pytest.raises(ValidationError) as exc_info:
            OrderItemCreate(
                product_name="Mouse",
                quantity=0,
                unit_price=Decimal("50.00"),
            )
        assert "greater than or equal to 1" in str(exc_info.value)

    def test_order_item_create_invalid_quantity_negative(self):
        """Testa que quantidade não pode ser negativa."""
        with pytest.raises(ValidationError):
            OrderItemCreate(
                product_name="Mouse",
                quantity=-1,
                unit_price=Decimal("50.00"),
            )

    def test_order_item_create_invalid_unit_price_negative(self):
        """Testa que preço não pode ser negativo."""
        with pytest.raises(ValidationError) as exc_info:
            OrderItemCreate(
                product_name="Mouse",
                quantity=1,
                unit_price=Decimal("-50.00"),
            )

    def test_order_item_create_missing_required_field(self):
        """Testa que product_name é obrigatório."""
        with pytest.raises(ValidationError):
            OrderItemCreate(
                quantity=1,
                unit_price=Decimal("50.00"),
            )


class TestOrderItemResponse:
    """Testes para o schema OrderItemResponse."""

    def test_valid_order_item_response(self):
        """Testa criação válida de resposta de item."""
        item_id = uuid.uuid4()
        item = OrderItemResponse(
            id=item_id,
            product_name="Notebook",
            quantity=1,
            unit_price=Decimal("1500.00"),
        )
        assert item.id == item_id
        assert item.product_name == "Notebook"
        assert item.quantity == 1
        assert item.unit_price == Decimal("1500.00")

    def test_order_item_response_from_attributes(self):
        """Testa configuração from_attributes."""
        assert OrderItemResponse.model_config["from_attributes"] is True


class TestOrderCreate:
    """Testes para o schema OrderCreate."""

    def test_valid_order_create(self):
        """Testa criação válida de pedido."""
        order = OrderCreate(
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
        assert order.customer_name == "João Silva"
        assert len(order.items) == 2

    def test_order_create_single_item(self):
        """Testa pedido com um único item."""
        order = OrderCreate(
            customer_name="Maria",
            items=[
                OrderItemCreate(
                    product_name="Teclado",
                    quantity=1,
                    unit_price=Decimal("200.00"),
                ),
            ],
        )
        assert len(order.items) == 1

    def test_order_create_no_items_invalid(self):
        """Testa que pedido sem items é inválido."""
        with pytest.raises(ValidationError) as exc_info:
            OrderCreate(
                customer_name="João Silva",
                items=[],
            )
        assert "at least 1 item" in str(exc_info.value)

    def test_order_create_missing_customer_name(self):
        """Testa que customer_name é obrigatório."""
        with pytest.raises(ValidationError):
            OrderCreate(
                items=[
                    OrderItemCreate(
                        product_name="Notebook",
                        quantity=1,
                        unit_price=Decimal("1500.00"),
                    ),
                ],
            )

    def test_order_create_missing_items(self):
        """Testa que items é obrigatório."""
        with pytest.raises(ValidationError):
            OrderCreate(
                customer_name="João Silva",
            )


class TestOrderResponse:
    """Testes para o schema OrderResponse."""

    def test_valid_order_response(self):
        """Testa criação válida de resposta de pedido."""
        order_id = uuid.uuid4()
        now = datetime.now()
        order = OrderResponse(
            id=order_id,
            customer_name="João Silva",
            status=OrderStatus.PENDING,
            total=Decimal("1600.00"),
            user_id="joao@example.com",
            items=[
                OrderItemResponse(
                    id=uuid.uuid4(),
                    product_name="Notebook",
                    quantity=1,
                    unit_price=Decimal("1500.00"),
                ),
                OrderItemResponse(
                    id=uuid.uuid4(),
                    product_name="Mouse",
                    quantity=2,
                    unit_price=Decimal("50.00"),
                ),
            ],
            created_at=now,
            updated_at=now,
        )
        assert order.id == order_id
        assert order.customer_name == "João Silva"
        assert order.status == OrderStatus.PENDING
        assert order.total == Decimal("1600.00")
        assert order.user_id == "joao@example.com"
        assert len(order.items) == 2

    def test_order_response_from_attributes(self):
        """Testa configuração from_attributes."""
        assert OrderResponse.model_config["from_attributes"] is True

    def test_order_response_all_fields_required(self):
        """Testa que todos os campos são obrigatórios."""
        with pytest.raises(ValidationError):
            OrderResponse(
                id=uuid.uuid4(),
                customer_name="João Silva",
                status=OrderStatus.PENDING,
                total=Decimal("1600.00"),
                user_id="joao@example.com",
                # items e created_at/updated_at faltam
            )


class TestOrderStatusUpdate:
    """Testes para o schema OrderStatusUpdate."""

    def test_valid_order_status_update(self):
        """Testa atualização válida de status."""
        update = OrderStatusUpdate(status=OrderStatus.CONFIRMED)
        assert update.status == OrderStatus.CONFIRMED

    def test_order_status_update_all_statuses(self):
        """Testa que todos os status são válidos."""
        for status in OrderStatus:
            update = OrderStatusUpdate(status=status)
            assert update.status == status

    def test_order_status_update_from_string(self):
        """Testa criação a partir de string."""
        update = OrderStatusUpdate(status="enviado")
        assert update.status == OrderStatus.SHIPPED

    def test_order_status_update_missing_status(self):
        """Testa que status é obrigatório."""
        with pytest.raises(ValidationError):
            OrderStatusUpdate()

    def test_order_status_update_invalid_status(self):
        """Testa que status inválido é rejeitado."""
        with pytest.raises(ValidationError):
            OrderStatusUpdate(status="invalid_status")