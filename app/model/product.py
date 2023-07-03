from typing import List, Optional
from sqlalchemy import Column, String, Float
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from app.model.cart_product import CartProduct

class Product(SQLModel, table=True):
    __tablename__= "product"

    product_id: str = Field(sa_column=Column("product_id", String, primary_key=True, nullable=False))
    product_name: str = Field(sa_column=Column("product_name", String, unique=True))
    description: str = Field(sa_column=Column("description", String))
    price: float = Field(sa_column=Column("price", Float))
    image: str = Field(sa_column=Column("image", String))
    
    brand_id: Optional[str] = Field(default=None, foreign_key="brand.brand_id")
    brand: Optional["Brand"] = Relationship(back_populates="product")
    
    cart: List["Cart"] = Relationship(back_populates="product", link_model=CartProduct)