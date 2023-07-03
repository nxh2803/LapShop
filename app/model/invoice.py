from typing import List, Optional
from sqlalchemy import Column, String, ForeignKey, ForeignKeyConstraint, Float
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
import uuid


class Invoice(SQLModel, table=True):
    __tablename__ = "invoice"

    invoice_id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )

    order_id_auto_generated: str = Field(
        sa_column=Column("order_id_auto_generated", String)
    )
    order_id: str = Field(sa_column=Column("order_id", String))

    order: Optional["Order"] = Relationship(back_populates="invoice")

    order_date: datetime = Field(default_factory=datetime.now)
    order_status: str = Field(sa_column=Column("order_status", String))
    payment_method: str = Field(sa_column=Column("payment_method", String))
    address: str = Field(sa_column=Column("address", String))
    total_amount: float = Field(sa_column=Column("total_amount", Float))
    user_id: str = Field(sa_column=Column("user_id", String, ForeignKey("user.id")))

    user: Optional["User"] = Relationship(back_populates="invoices")

    __table_args__ = (
        ForeignKeyConstraint(
            ["order_id_auto_generated", "order_id"],
            ["order.order_id_auto_generated", "order.order_id"],
        ),
    )
