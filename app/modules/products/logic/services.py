# app/modules/products/logic/services.py
"""Servicios relacionados con productos."""

from __future__ import annotations

from app.config.settings import settings
from app.libraries.customs.base_service import BaseService

from ..data.dao import ProductDAO


class ProductService(BaseService):
    """Capa de lógica para productos."""

    def __init__(self) -> None:
        super().__init__(ProductDAO())

    def list_products(self, company_id: str | None = None):
        """Obtiene productos filtrando por empresa cuando aplica."""
        target_company = company_id or settings.DEFAULT_COMPANY_ID
        if target_company:
            return self.dao.filter(company_id=target_company)
        return self.dao.get_all()
