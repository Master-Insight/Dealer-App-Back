# app/modules/quotations/logic/services.py
from __future__ import annotations

from typing import Dict, Optional

from app.config.settings import settings
from app.libraries.customs.base_service import BaseService
from app.libraries.exceptions.app_exceptions import (
    AuthError,
    NotFoundError,
    ValidationError,
)

from ..data.dao import QuotationDAO


class QuotationService(BaseService):
    def __init__(self) -> None:
        super().__init__(QuotationDAO())

    def list_quotations(
        self,
        *,
        profile: Dict,
        company_id: Optional[str] = None,
        deal_id: Optional[str] = None,
    ):
        target_company = (
            company_id or profile.get("company_id") or settings.DEFAULT_COMPANY_ID
        )

        if profile.get("role") == "root" and not target_company:
            return self.dao.get_all()

        if not target_company:
            raise ValidationError("Debes indicar una empresa para ver cotizaciones")

        if (
            profile.get("role") == "admin"
            and company_id
            and company_id != profile.get("company_id")
        ):
            raise AuthError("No puedes consultar cotizaciones de otra empresa")

        filters = {
            "company_id": target_company,
            "deal_id": deal_id,
        }

        if profile.get("role") == "user":
            filters["advisor_id"] = profile.get("id")

        return self.dao.filter_by(filters)

    def create_quotation(self, profile: Dict, data: Dict):
        target_company = (
            data.get("company_id")
            or profile.get("company_id")
            or settings.DEFAULT_COMPANY_ID
        )

        if not target_company:
            raise ValidationError("Debes indicar una empresa para la cotización")

        if (
            profile.get("role") == "admin"
            and data.get("company_id")
            and data["company_id"] != profile.get("company_id")
        ):
            raise AuthError("No puedes crear cotizaciones para otra empresa")

        if profile.get("role") == "user":
            data["advisor_id"] = profile.get("id")

        data["company_id"] = target_company

        amount = data.get("amount")
        if amount is None or float(amount) <= 0:
            raise ValidationError("El monto de la cotización debe ser mayor a cero")

        metadata = {
            "company_id": target_company,
            "deal_id": data.get("deal_id"),
            "product_id": data.get("product_id"),
        }
        return self.create(data, audit_metadata=metadata)

    def update_quotation(self, profile: Dict, quotation_id: str, data: Dict):
        quotation = self.dao.get_by_id(quotation_id)
        if not quotation:
            raise NotFoundError("Cotización no encontrada")

        if profile.get("role") == "user" and quotation.get("advisor_id") != profile.get(
            "id"
        ):
            raise AuthError("No puedes modificar esta cotización")

        if profile.get("role") == "admin" and quotation.get(
            "company_id"
        ) != profile.get("company_id"):
            raise AuthError("No puedes modificar cotizaciones de otra empresa")

        if (
            "amount" in data
            and data["amount"] is not None
            and float(data["amount"]) <= 0
        ):
            raise ValidationError("El monto debe ser mayor a cero")

        metadata = {
            "company_id": quotation.get("company_id"),
            "deal_id": quotation.get("deal_id"),
            "product_id": quotation.get("product_id"),
        }
        return self.update(quotation_id, data, audit_metadata=metadata)

    def delete_quotation(self, profile: Dict, quotation_id: str):
        quotation = self.dao.get_by_id(quotation_id)
        if not quotation:
            raise NotFoundError("Cotización no encontrada")

        if profile.get("role") == "user":
            raise AuthError("No tienes permisos para eliminar cotizaciones")

        if profile.get("role") == "admin" and quotation.get(
            "company_id"
        ) != profile.get("company_id"):
            raise AuthError("No puedes eliminar cotizaciones de otra empresa")

        metadata = {
            "company_id": quotation.get("company_id"),
            "deal_id": quotation.get("deal_id"),
            "product_id": quotation.get("product_id"),
        }
        return self.delete(quotation_id, audit_metadata=metadata)
