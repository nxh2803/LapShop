from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer


class CartProduct(SQLModel, table=True):
    __tablename__ = "cart_product"

    cart_id: Optional[str] = Field(None, foreign_key="cart.cart_id", primary_key=True)
    product_id: Optional[str] = Field(
        None, foreign_key="product.product_id", primary_key=True
    )

    quantity: int = Field(sa_column=Column("quantity", Integer))


