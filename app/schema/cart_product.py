from pydantic import BaseModel


class CartProductBase(BaseModel):
    cart_id: str


class CartProductRequest(CartProductBase):
    quantity: int
    product_id: str


class CartProductResponse(CartProductBase):
    quantity: int
    product_id: str
    
class UpdateCartProduct(BaseModel):
    quantity: int
