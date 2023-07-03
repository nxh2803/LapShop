from sqlalchemy.future import select
from app.model import Order, Invoice, Cart
from app.config import db
from sqlalchemy.orm import Session
from app.schema.schema import RegisterSchema, UserSchema
from sqlalchemy import update
from uuid import UUID


# class InvoiceService:
#     @staticmethod
#     async def get_invoices():
#         query = (
#             select(
#                 Invoice.order_date,
#                 Invoice.payment_method,
#                 Invoice.address,
#                 Invoice.total_amount,
#                 Cart.user_id,
#                 Cart.cart_id,
#                 Order.order_id,
#             )
#             .join_from(Invoice, Order)
#             .join(Cart)
#         )
#         result = await db.execute(query)
#         return result.all()