from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from typing import List
from app.model.cart_product import CartProduct
from app.config import db, commit_rollback
from app.schema.cart_product import CartProductRequest,CartProductResponse,UpdateCartProduct
from sqlalchemy.future import select
from sqlalchemy import delete
from app.model.cart_product import CartProduct
from uuid import UUID

router = APIRouter(prefix="", tags=["Cart Product"])


@router.post("/addtocart")
async def addtocart(cartproduct_data: CartProductRequest):
    cartproduct = CartProduct(**cartproduct_data.dict())

    existing_cartproduct = await check_existing_cart_product(
        cartproduct.cart_id, cartproduct.product_id
    )
    if existing_cartproduct:
        existing_cartproduct.quantity += cartproduct.quantity
        await commit_rollback()
        await db.session.refresh(existing_cartproduct)
        return {"message": "Quantity updated successfully"}

    db.session.add(cartproduct)
    await commit_rollback()
    await db.session.refresh(cartproduct)
    return {"message": "Added to cart successfully"}


@router.get("/carts", response_model=List[CartProductResponse])
async def carts():
    query = select(CartProduct)
    result = await db.session.execute(query)
    carts = result.scalars().all()
    return carts


@router.put("/updatefromcart/{cart_id}/{product_id}")
async def update_from_cart(
    cart_id: UUID, product_id: int, cartproduct_data: UpdateCartProduct
):
    try:
        cartproduct = await check_existing_cart_product(str(cart_id), str(product_id))
        if not cartproduct:
            raise HTTPException(status_code=404, detail="Cart product not found")

        cartproduct.quantity = cartproduct_data.quantity
        await commit_rollback()
        return {"message": "Cart product updated successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/deletefromcart/{cart_id}/{product_id}")
async def delete_from_cart(cart_id: UUID, product_id: str):
    try:
        cartproduct = await check_existing_cart_product(str(cart_id), str(product_id))
        if not cartproduct:
            raise HTTPException(status_code=404, detail="Cart product not found")

        delete_cartproduct_query = delete(CartProduct).where(
            CartProduct.cart_id == str(cart_id),
            CartProduct.product_id == str(product_id),
        )
        await db.session.execute(delete_cartproduct_query)
        await commit_rollback()

        return {"message": "Cart product removed successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# @router.delete("/deletefromcart/{cart_id}/{product_id}")
# async def delete_from_cart(cart_id: UUID, product_ids: List[str]):
#     try:
#         for product_id in product_ids:
#             cartproduct = await check_existing_cart_product(
#                 str(cart_id), str(product_id)
#             )
#             if not cartproduct:
#                 raise HTTPException(
#                     status_code=404,
#                     detail=f"Cart product with product_id {product_id} not found",
#                 )

#             delete_cartproduct_query = delete(CartProduct).where(
#                 CartProduct.cart_id == str(cart_id),
#                 CartProduct.product_id == str(product_id),
#             )
#             await db.session.execute(delete_cartproduct_query)

#         await commit_rollback()

#         return {"message": "Cart products removed successfully"}
#     except SQLAlchemyError as e:
#         raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/cartByCartId/{cart_id}", response_model=List[CartProductResponse])
async def cartproduct_by_productId(cart_id: str):
    query = select(CartProduct).where(CartProduct.cart_id == cart_id)
    result = await db.session.execute(query)
    cartproduct = result.scalars().all()
    if not cartproduct:
        raise HTTPException(status_code=404, detail="Cart product not found")
    return cartproduct


async def check_existing_cart_product(cart_id: str, product_id: str):
    query = select(CartProduct).filter(
        CartProduct.cart_id == cart_id, CartProduct.product_id == product_id
    )
    result = await db.session.execute(query)
    return result.scalar_one_or_none()
