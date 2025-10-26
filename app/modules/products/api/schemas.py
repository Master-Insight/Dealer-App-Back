# app/modules/products/api/schemas.py
from typing import List, Optional, Union
from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class ProductState(str, Enum):
    usado = "Usado"
    nuevo = "Nuevo"
    areparar = "A reparar"


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
    state: Optional[ProductState] = None
    description: Optional[str] = None
    active: Optional[bool] = False
    photos_url: Optional[List[str]] = None
    price: Optional[float] = None
    labels: Optional[List[str]] = None
    vehicle_type: Optional[ProductTypes] = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    created_at: datetime
    update: Optional[datetime] = None

    class Config:
        from_attributes = True


class ResponseModel(BaseModel):
    success: bool
    message: str
    data: Optional[Union[Product, List[Product], dict, str]] = None
