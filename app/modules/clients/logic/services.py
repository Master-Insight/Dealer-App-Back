# app\modules\clients\logic\services.py
"""Servicios de negocio para clientes."""

from __future__ import annotations

from typing import Dict, Optional

from app.libraries.customs.base_service import BaseService
from app.libraries.exceptions.app_exceptions import (
    AuthError,
    NotFoundError,
    ValidationError,
)
from app.config.settings import settings

from ..data.dao import ClientDAO


class ClientService(BaseService):
    def __init__(self) -> None:
        super().__init__(ClientDAO())

    def list_clients(self, *, profile: Dict, company_id: Optional[str] = None):
        target_company = company_id or profile.get("company_id")
        if not target_company:
            return self.dao.get_all()
        return self.dao.filter(company_id=target_company)

    def search_clients(self, *, profile: Dict, term: str):
        company_id = profile.get("company_id")
        if not company_id:
            raise AuthError("El usuario no tiene empresa asignada")
        return self.dao.search(company_id=company_id, term=term)

    def create_client(self, profile: Dict, data: Dict):
        target_company = (
            data.get("company_id")
            or profile.get("company_id")
            or settings.DEFAULT_COMPANY_ID
        )

        if not target_company:
            raise ValidationError("Debe especificar una compañía para el cliente")

        data["company_id"] = target_company
        metadata = {"company_id": target_company}
        return self.create(data, audit_metadata=metadata)

    def update_client(self, profile: Dict, client_id: str, data: Dict):
        client = self.dao.get_by_id(client_id)
        if not client:
            raise NotFoundError("Cliente no encontrado")

        if profile.get("role") == "user" and client.get("company_id") != profile.get(
            "company_id"
        ):
            raise AuthError("No puedes editar clientes de otra empresa")

        metadata = {"company_id": client.get("company_id")}
        return self.update(client_id, data, audit_metadata=metadata)

    def delete_client(self, profile: Dict, client_id: str):
        client = self.dao.get_by_id(client_id)
        if not client:
            raise NotFoundError("Cliente no encontrado")

        if profile.get("role") == "user" and client.get("company_id") != profile.get(
            "company_id"
        ):
            raise AuthError("No puedes eliminar clientes de otra empresa")

        metadata = {"company_id": client.get("company_id")}
        return self.delete(client_id, audit_metadata=metadata)
