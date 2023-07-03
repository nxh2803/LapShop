from typing import List, Optional
from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field, Relationship
from sqlmodel import SQLModel, Field


class Brand(SQLModel, table=True):
    __tablename__ = "brand"

    brand_id: Optional[str] = Field(None, primary_key=True, nullable=False)
    brand_name: str = Field(sa_column=Column("brand_name", String, unique=True))
    brand_description: str = Field(
        sa_column=Column("brand_description", String, unique=True)
    )

    product: List["Product"] = Relationship(
        sa_relationship_kwargs={"uselist": True}, back_populates="brand"
    )
