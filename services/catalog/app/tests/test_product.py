from decimal import Decimal

import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product
from app.schemas import ProductCreate
from app.services.product import create_product, get_product_by_ean, list_products


async def clear_products_table(session: AsyncSession) -> None:
    await session.execute(delete(Product))
    await session.commit()


@pytest.fixture(autouse=True)
async def cleanup_products(db: AsyncSession):
    yield
    await clear_products_table(db)


@pytest.mark.asyncio
async def test_create_product(db: AsyncSession):
    payload = ProductCreate(
        ean="7894900011517",
        name="Notebook X",
        unit_price=Decimal("4500.00"),
    )

    product = await create_product(db, payload)

    assert product.ean == payload.ean
    assert product.name == payload.name
    assert product.unit_price == payload.unit_price


@pytest.mark.asyncio
async def test_get_product_by_ean(db: AsyncSession):
    payload = ProductCreate(
        ean="7894900011517",
        name="Notebook X",
        unit_price=Decimal("4500.00"),
    )
    created = await create_product(db, payload)

    fetched = await get_product_by_ean(db, created.ean)

    assert fetched is not None
    assert fetched.ean == created.ean


@pytest.mark.asyncio
async def test_list_products(db: AsyncSession):
    await create_product(
        db,
        ProductCreate(ean="7894900011517", name="Notebook X", unit_price=Decimal("4500.00")),
    )
    await create_product(
        db,
        ProductCreate(ean="7894900011524", name="Mouse Y", unit_price=Decimal("120.00")),
    )

    products = await list_products(db, skip=0, limit=10)

    assert len(products) == 2
    assert any(product.ean == "7894900011517" for product in products)
    assert any(product.ean == "7894900011524" for product in products)
