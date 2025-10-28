# app/modules/products/api/schemas.py
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ProductState(str, Enum):
    disponible = "Fisponible"
    reservado = "Reservado"
    vendido = "Vendido"
    baja = "Baja"


class ProductFuelType(str, Enum):
    nafta = "Nafta"
    gas = "Gas"
    diesel = "Diesel"
    electrico = "Eléctrico"


class ProductTransmision(str, Enum):
    manual = "Manual"
    automatica = "Automática"


class ProductTypes(str, Enum):
    auto = "Auto"
    moto = "Moto"
    camioneta = "Camioneta"
    camion = "Camión"


class ProductBase(BaseModel):
    company_id: str = Field(..., description="Empresa dueña del vehículo")
    brand: str
    model: str
    variant: Optional[str] = None
    year: Optional[int] = None
    mileage: Optional[int] = None
    fuel_type: Optional[ProductFuelType] = None
    transmission: Optional[ProductTransmision] = None
    color: Optional[str] = None
    doors: Optional[int] = None
    location: Optional[str] = None
    state: Optional[ProductState] = Field(
        default=ProductState.disponible,
        description="Estado comercial del vehículo",
    )
    description: Optional[str] = None
    active: Optional[bool] = False
    photos_url: Optional[List[str]] = None
    price: Optional[float] = None
    labels: Optional[List[str]] = None
    vehicle_type: Optional[ProductTypes] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    status: Optional[ProductState] = None


class Product(ProductBase):
    id: str
    created_at: Optional[datetime] = None
    update: Optional[datetime] = None

    class Config:
        from_attributes = True
