from datetime import datetime
from pydantic import BaseModel
from typing import TypeVar, Optional, List

T = TypeVar('T')

class OrderBase(BaseModel):
    order_id: Optional[str] = None

class OrderResponse(OrderBase):
    order_id: str
    
class OrderItemResponse(BaseModel):
    product_id: str
    quantity: int
    cart_id: str
    
class OrderRequest(BaseModel):
    # order_date: datetime = datetime.now().replace(tzinfo=None)
    product_id: str
    quantity: int
    cart_id: str

class OrderIdSearchResult(BaseModel):
    order_id: str
    order_id_auto_generated: str

class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None


