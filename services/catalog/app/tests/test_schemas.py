from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas import ProductCreate


class TestProductCreate:
    def test_valid_product(self):
        product = ProductCreate(
            ean="7894900011517",
            name="Notebook X",
            unit_price=Decimal("4500.00"),
        )

        assert product.ean == "7894900011517"
        assert product.name == "Notebook X"
        assert product.unit_price == Decimal("4500.00")

    def test_invalid_ean(self):
        with pytest.raises(ValidationError):
            ProductCreate(
                ean="ABC123",
                name="Produto",
                unit_price=Decimal("10.00"),
            )

    def test_invalid_price(self):
        with pytest.raises(ValidationError):
            ProductCreate(
                ean="7894900011517",
                name="Produto",
                unit_price=Decimal("0"),
            )
