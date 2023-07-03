from app.model.cart_product import CartProduct
from app.repository.base_repo import BaseRepo

class CartProductRepository(BaseRepo):
    model = CartProduct