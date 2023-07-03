from app.model.cart import Cart
from app.repository.base_repo import BaseRepo

class CartRepository(BaseRepo):
    model = Cart