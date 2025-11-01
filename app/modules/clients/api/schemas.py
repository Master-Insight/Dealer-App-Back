# app\modules\clients\api\schemas.py
"""Esquemas Pydantic para clientes."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ClientBase(BaseModel):
    company_id: Optional[str] = Field(
        default=None, description="Empresa asociada al cliente"
    )
    name: str = Field(..., description="Nombre completo del cliente")
    phone: Optional[str] = Field(
        default=None, description="Teléfono principal del cliente"
    )
    email: Optional[EmailStr] = Field(default=None, description="Correo de contacto")
    dni: Optional[str] = Field(default=None, description="Documento de identidad")
    address: Optional[str] = Field(default=None, description="Direcciòn de cliente")
    city: Optional[str] = Field(
        default=None, description="Ciudad de residencia del cliente"
    )
    province: Optional[str] = Field(
        default=None, description="Provincia de residencia del cliente"
    )


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    dni: Optional[str] = None


class Client(ClientBase):
    id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
