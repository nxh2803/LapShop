from typing import Optional
from sqlalchemy import Column, String, Float, Integer, UniqueConstraint
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlmodel import ForeignKey
import uuid


class Order(SQLModel, table=True):
    __tablename__ = "order"

    order_id_auto_generated: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        sa_column=Column("order_id_auto_generated", String, primary_key=True),
    )

    order_id: str = Field(sa_column=Column("order_id", String))

    __table_args__ = (
        UniqueConstraint("order_id_auto_generated", "order_id", name="unique_order_id"),
    )

    invoice: Optional["Invoice"] = Relationship(back_populates="order")

    product_id: str = Field(sa_column=Column("product_id", String))
    quantity: int = Field(sa_column=Column("quantity", Integer))

    cart_id: Optional[str] = Field(default=None, foreign_key="cart.cart_id")
    cart: Optional["Cart"] = Relationship(back_populates="order")
