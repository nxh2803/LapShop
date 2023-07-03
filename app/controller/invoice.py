from fastapi import APIRouter, HTTPException
from app.model.invoice import Invoice
from app.model.order import Order
from app.config import db, commit_rollback
from sqlalchemy.future import select
from app.schema.invoice import InvoiceResponse, InvoiceRequest, ResponseSchema, InvoiceAddressRequest
from typing import List

router = APIRouter(prefix="", tags=["Invoice"])


@router.post("/invoice", response_model=ResponseSchema)
async def create_invoice(product_data: InvoiceRequest):
    invoice = Invoice(**product_data.dict())
    db.session.add(invoice)
    await commit_rollback()
    await db.session.refresh(invoice)
    return ResponseSchema(detail="Successfully fetch data!")


# @router.post("/invoice", response_model=ResponseSchema)
# async def create_invoice(product_data: List[InvoiceRequest]):
#     invoices = []

#     for data in product_data:
#         invoice = Invoice(**data.dict())
#         invoices.append(invoice)
#         db.session.add(invoice)

#     await commit_rollback()

#     for invoice in invoices:
#         await db.session.refresh(invoice)

#     return ResponseSchema(detail="Successfully fetch data!")


# @router.get("/invoice/{invoice_id}", response_model=InvoiceResponse)
# async def get_invoice_by_id(invoice_id: str):
#     query = select(Invoice).where(Invoice.invoice_id == invoice_id)
#     result = await db.session.execute(query)
#     invoice = result.scalars()

# if invoice:
#     return invoice
# else:
#     raise HTTPException(status_code=404, detail="Invoice not found")


@router.get(
    "/invoices", response_model=List[InvoiceResponse], response_model_exclude_none=True
)
async def get_invoices():
    query = select(Invoice)
    result = await db.session.execute(query)
    invoices = result.scalars().all()
    return invoices


@router.get(
    "/invoices/{user_id}",
    response_model=List[InvoiceResponse],
    response_model_exclude_none=True,
)
async def get_invoices_by_user_id(user_id: str):
    query = select(Invoice).where(Invoice.user_id == user_id)
    result = await db.session.execute(query)
    invoices = result.scalars().all()
    return invoices


@router.put("/invoice/{invoice_id}/address", response_model=ResponseSchema)
async def update_invoice_address(invoice_id: str, invoice_data: InvoiceAddressRequest):
    query = select(Invoice).where(Invoice.invoice_id == invoice_id)
    result = await db.session.execute(query)
    invoice = result.scalars().first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    invoice.address = invoice_data.address
    await commit_rollback()

    return ResponseSchema(detail="Address updated successfully!")

@router.delete("/invoice/{order_id}", response_model=ResponseSchema)
async def delete_invoice_by_order_id(order_id: str):
    query = select(Invoice).where(Invoice.order_id == order_id)
    result = await db.session.execute(query)
    invoice = result.scalars().first()

    if invoice:
        await db.session.delete(invoice)
        await commit_rollback()
        return ResponseSchema(detail="Invoice deleted successfully!")
    else:
        raise HTTPException(status_code=404, detail="Invoice not found")
