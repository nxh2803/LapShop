from pydantic import BaseModel
from typing import Optional


class CartBase(BaseModel):
    cart_id: str


class CartResponse(CartBase):
    user_id: Optional[str] = None
