# app\modules\deals\api\schemas.py
"""Esquemas para gestiones/comerciales."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class DealStatus(str, Enum):
    pendiente = "pendiente"
    asignada = "asignada"
    realizada = "realizada"
    perdida = "perdida"
    en_cobro = "en_cobro"


class DealBase(BaseModel):
    company_id: str = Field(..., description="Empresa dueña de la gestión")
    advisor_id: Optional[str] = Field(None, description="Usuario responsable")
    client_id: str = Field(..., description="Cliente asociado")
    product_id: Optional[str] = Field(
        default=None, description="Producto asociado (opcional)"
    )
    scheduled_for: Optional[datetime] = Field(
        None, description="Fecha y hora de la cita con el cliente"
    )
    status: DealStatus = Field(default=DealStatus.pendiente)
    notes: Optional[str] = None


class DealCreate(DealBase):
    pass


class DealUpdate(BaseModel):
    advisor_id: Optional[str] = None
    client_id: Optional[str] = None
    product_id: Optional[str] = None
    scheduled_for: Optional[datetime] = None
    status: Optional[DealStatus] = None
    notes: Optional[str] = None


class Deal(DealBase):
    id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DealEmailRequest(BaseModel):
    email: str = Field(..., description="Correo del cliente a notificar")
    subject: str = Field(default="Confirmación de cita")
    message: Optional[str] = Field(
        default=None,
        description="Mensaje personalizado, si se omite se genera uno genérico",
    )
