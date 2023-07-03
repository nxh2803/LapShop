from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import List
from app.model.cart import Cart, CartProduct
from app.config import db, commit_rollback
from app.schema.cart import CartResponse

router = APIRouter(prefix="", tags=["Cart"])


@router.get("/cart", response_model=List[CartResponse])
async def cart():
    query = select(Cart)
    result = await db.session.execute(query)
    cart = result.scalars().all()
    return cart


@router.get("/cart/{user_id}", response_model=CartResponse)
async def cart_by_id(user_id: str):
    query = select(Cart).where(Cart.user_id == user_id)
    result = await db.session.execute(query)
    cart = result.scalars().first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.delete("/cart", status_code=204)
async def delete_all_carts():
    try:
        delete_cart_product_query = delete(CartProduct)
        await db.session.execute(delete_cart_product_query)
        delete_cart_query = delete(Cart)
        await db.session.execute(delete_cart_query)
        await commit_rollback()
        return None

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
