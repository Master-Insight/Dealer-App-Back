# app/modules/analytics/api/schemas.py
from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field


class DealsSummary(BaseModel):
    total: int = Field(..., description="Total de gestiones registradas")
    by_status: Dict[str, int] = Field(
        default_factory=dict, description="Cantidad de gestiones por estado"
    )
    conversion_rate: float = Field(
        ..., description="Porcentaje de gestiones marcadas como realizadas"
    )
    upcoming_next_7_days: int = Field(
        ..., description="Cantidad de gestiones próximas en los próximos 7 días"
    )


class ProductsSummary(BaseModel):
    total: int = Field(..., description="Total de vehículos publicados")
    by_status: Dict[str, int] = Field(
        default_factory=dict, description="Cantidad de vehículos por estado"
    )


class ClientsSummary(BaseModel):
    total: int = Field(..., description="Cantidad total de clientes")
    new_last_30_days: int = Field(
        ..., description="Clientes creados en los últimos 30 días"
    )


class AnalyticsSummary(BaseModel):
    company_id: str = Field(
        ..., description="Empresa para la cual se generó el resumen"
    )
    generated_at: datetime = Field(
        ..., description="Fecha y hora de generación del informe"
    )
    deals: DealsSummary
    products: ProductsSummary
    clients: ClientsSummary
    advisor_filter_applied: bool = Field(
        ..., description="Indica si se filtró por asesor por las credenciales"
    )


class ActivityTrendPoint(BaseModel):
    date: datetime
    deals_created: int
    new_clients: int


class AnalyticsDetail(AnalyticsSummary):
    activity_trend: Optional[list[ActivityTrendPoint]] = Field(
        default=None,
        description="Evolución diaria de gestiones y clientes",
    )
