from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product
from app.schemas import ProductCreate


async def get_product_by_ean(db: AsyncSession, ean: str) -> Product | None:
    result = await db.execute(select(Product).where(Product.ean == ean))
    return result.scalar_one_or_none()


async def list_products(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Product]:
    result = await db.execute(
        select(Product).offset(skip).limit(limit).order_by(Product.created_at.desc())
    )
    return list(result.scalars().all())


async def create_product(db: AsyncSession, payload: ProductCreate) -> Product:
    product = Product(
        ean=payload.ean,
        name=payload.name,
        unit_price=payload.unit_price,
    )
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def update_product(db: AsyncSession, ean: str, payload: ProductCreate) -> Product | None:
    product = await get_product_by_ean(db, ean)
    if not product:
        return None

    product.ean = payload.ean
    product.name = payload.name
    product.unit_price = payload.unit_price
    await db.commit()
    await db.refresh(product)
    return product


async def delete_product(db: AsyncSession, ean: str) -> bool:
    product = await get_product_by_ean(db, ean)
    if not product:
        return False

    await db.delete(product)
    await db.commit()
    return True
