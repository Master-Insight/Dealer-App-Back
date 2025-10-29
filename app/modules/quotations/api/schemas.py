# app/modules/quotations/api/schemas.py
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, condecimal


class QuotationBase(BaseModel):
    company_id: Optional[str] = Field(
        default=None, description="Empresa dueña de la cotización"
    )
    deal_id: Optional[str] = Field(
        default=None, description="Gestión asociada a la cotización"
    )
    product_id: Optional[str] = Field(default=None, description="Producto asociado")
    advisor_id: Optional[str] = Field(
        default=None, description="Asesor responsable de la cotización"
    )
    amount: condecimal(gt=0, max_digits=12, decimal_places=2) = Field(
        ..., description="Monto total presupuestado"
    )
    currency: str = Field(default="ARS", description="Moneda de la cotización")
    expires_at: Optional[date] = Field(
        default=None, description="Fecha de vencimiento del presupuesto"
    )
    notes: Optional[str] = Field(default=None, description="Notas adicionales")


class QuotationCreate(QuotationBase):
    pass


class QuotationUpdate(BaseModel):
    deal_id: Optional[str] = None
    product_id: Optional[str] = None
    advisor_id: Optional[str] = None
    amount: Optional[Decimal] = Field(default=None, gt=0)
    currency: Optional[str] = None
    expires_at: Optional[date] = None
    notes: Optional[str] = None


class Quotation(QuotationBase):
    id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
