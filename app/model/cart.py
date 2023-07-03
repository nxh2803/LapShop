from typing import List, Optional
from sqlalchemy import Column, String
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

from app.model.mixins import TimeMixin
from app.model.cart_product import CartProduct


class Cart(SQLModel, TimeMixin, table=True):
    __tablename__ = "cart"

    cart_id: Optional[str] = Field(None, primary_key=True, nullable=False)

    user_id: Optional[str] = Field(default=None, foreign_key="user.id", unique=True)
    user: Optional["User"] = Relationship(back_populates="cart")
    
    product: List["Product"] = Relationship(
        back_populates="cart", link_model=CartProduct
    )
    
    order: List["Order"] = Relationship(
        sa_relationship_kwargs={"uselist": True}, back_populates="cart"
    )
