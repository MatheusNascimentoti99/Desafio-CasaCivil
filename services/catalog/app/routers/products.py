from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import ProductCreate, ProductResponse
from app.services import create_product, get_product_by_ean, list_products

router = APIRouter(prefix="/api/catalog/products", tags=["catalog"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_new_product(payload: ProductCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_product_by_ean(db, payload.ean)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="EAN já cadastrado",
        )

    product = await create_product(db, payload)
    return product


@router.get("/", response_model=list[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    return await list_products(db, skip=skip, limit=limit)


@router.get("/{ean}", response_model=ProductResponse)
async def get_product(ean: str, db: AsyncSession = Depends(get_db)):
    product = await get_product_by_ean(db, ean)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado",
        )
    return product
