# app/modules/products/api/schemas.py
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class ProductBase(BaseModel):
    brand: str
    model: str
    variant: Optional[str] = None
    year: Optional[int] = None
    mileage: Optional[int] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    color: Optional[str] = None
    doors: Optional[int] = None
    ubicacion: Optional[str] = None
    estado: Optional[str] = None
    descripcion: Optional[str] = None
    price: Optional[float] = None
    labels: Optional[List[str]] = None
    vehicle_type: Optional[str] = None
    fotos_url: Optional[List[str]] = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    created_at: datetime
    update: Optional[datetime] = None
    activo: bool

    class Config:
        from_attributes = True
