# app\modules\clients\api\controller.py
"""Controlador HTTP para clientes."""

from __future__ import annotations

from typing import Dict, Optional

from app.libraries.utils.response_builder import ResponseBuilder

from ..logic.services import ClientService
from .schemas import ClientCreate, ClientUpdate


class ClientController:
    def __init__(self) -> None:
        self.service = ClientService()

    def list_clients(self, profile: Dict, company_id: Optional[str]):
        data = self.service.list_clients(profile=profile, company_id=company_id)
        return ResponseBuilder.success(data, "Clientes obtenidos correctamente")

    def search_clients(self, profile: Dict, term: str):
        data = self.service.search_clients(profile=profile, term=term)
        return ResponseBuilder.success(data, "Resultados de búsqueda obtenidos")

    def create_client(self, profile: Dict, payload: ClientCreate):
        data_dict = payload.model_dump(exclude_unset=True)
        created = self.service.create_client(profile, data_dict)
        return ResponseBuilder.success(created, "Cliente creado correctamente")

    def update_client(self, profile: Dict, client_id: str, payload: ClientUpdate):
        data_dict = payload.model_dump(exclude_unset=True)
        updated = self.service.update_client(profile, client_id, data_dict)
        return ResponseBuilder.success(updated, "Cliente actualizado correctamente")

    def delete_client(self, profile: Dict, client_id: str):
        deleted = self.service.delete_client(profile, client_id)
        return ResponseBuilder.success(deleted, "Cliente eliminado correctamente")
