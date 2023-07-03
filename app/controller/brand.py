from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.future import select
from typing import List
from app.model.brand import Brand
from app.config import db, commit_rollback

from app.schema.brand import BrandResponse, BrandListResponse

router = APIRouter(prefix="", tags=["Brand"])

@router.get("/brand/{brand_id}", response_model=BrandResponse)
async def get_brand(brand_id: str):
    query = select(Brand).where(Brand.brand_id == brand_id)
    result = await db.session.execute(query)
    brand = result.scalars().first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand

@router.get("/brands", response_model=List[BrandListResponse])
async def list_brand():
    query = select(Brand)
    result = await db.session.execute(query)
    brands = result.scalars().all()
    return brands
